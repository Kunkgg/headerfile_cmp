import json
import pathlib
import logging
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from functools import cached_property
from typing import Dict, List, NamedTuple, Tuple

import CppHeaderParser

import common.init_log
from common.utils import readlines
from headerfile_formatter import combine_splited_line

logger = logging.getLogger(__name__)


class SyntaxType(Enum):
    TEXT = "text"
    INCLUDE = "include"
    DEFINE = "define"
    ENUM = "enum"
    VARIABLE = "variable"
    STRUCT = "variable"


@dataclass
class SyntaxElement:
    syntaxType: SyntaxType
    name: str
    content: List[str] = field(repr=False)


@dataclass
class SyntaxElementCollection:
    elements: List[SyntaxElement] = field(default_factory=list)


@dataclass
class ParsedHeaderFile:
    file: str
    includes: SyntaxElementCollection
    defines: SyntaxElementCollection
    enums: SyntaxElementCollection
    variables: SyntaxElementCollection
    structs: SyntaxElementCollection

    def __repr__(self):
        fn = pathlib.Path(self.file).name
        includes_count = len(self.includes.elements)
        defines_count = len(self.defines.elements)
        enums_count = len(self.enums.elements)
        variables_count = len(self.variables.elements)
        structs_count = len(self.structs.elements)
        return (
            f"<ParsedHeaderFile: {fn} [includes: {includes_count}]"
            + f" [defines: {defines_count}] [enums: {enums_count}]"
            + f" [variables: {variables_count}] [structs: {structs_count}]>"
        )


class HeaderFileParser:
    def __init__(self, fn: str):
        self.fn = fn

    def parse(self):
        return ParsedHeaderFile(
            file=self.fn,
            includes=self.includes,
            defines=self.defines,
            enums=self.enums,
            variables=self.variables,
            structs=self.structs,
        )

    def to_dict(self) -> Dict:
        return asdict(self.parse())

    def to_json(self, fn: str, encoding: str = "utf-8"):
        class ParsedHeaderFileJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, SyntaxType):
                    return obj.value
                return json.JSONEncoder.default(self, obj)

        with open(fn, "w", encoding=encoding) as fp:
            json.dump(self.to_dict(), fp, indent=2, cls=ParsedHeaderFileJSONEncoder)
        logger.info(f"Dumped headerfile parse result to: {fn}")

    @cached_property
    def lines(self) -> List[str]:
        return readlines(self.fn)

    @cached_property
    def _ast(self):
        logger.debug(f"Parsered {self.fn} by robotpy-cppheaderparser")
        return CppHeaderParser.CppHeader(self.fn)

    @cached_property
    def includes(self) -> SyntaxElementCollection:
        extracted_includes = [
            SyntaxElement(SyntaxType.INCLUDE, include, [])
            for include in self._ast.includes
        ]
        logger.debug(f"Extracted includes: {len(extracted_includes)}")
        return SyntaxElementCollection(extracted_includes)

    @cached_property
    def defines(self) -> SyntaxElementCollection:
        extracted_defines = [
            self.extract_define(define) for define in self._ast.defines
        ]
        logger.debug(f"Extracted enums: {len(extracted_defines)}")
        return SyntaxElementCollection(extracted_defines)

    @cached_property
    def enums(self) -> SyntaxElementCollection:
        extracted_enums = [self.extract_enum(enum_) for enum_ in self._ast.enums]
        logger.debug(f"Extracted enums: {len(extracted_enums)}")
        return SyntaxElementCollection(extracted_enums)

    @cached_property
    def variables(self):
        extracted_variables = [
            self.extract_variable(variable) for variable in self._ast.variables
        ]
        logger.debug(f"Extracted variables: {len(extracted_variables)}")
        return SyntaxElementCollection(extracted_variables)

    @cached_property
    def structs(self):
        extracted_structs = [
            self.extract_struct(ast_class)
            for ast_class_name, ast_class in self._ast.classes.items()
            if "anon-struct" not in ast_class_name
        ]
        logger.debug(f"Extracted structs: {len(extracted_structs)}")
        return SyntaxElementCollection(extracted_structs)

    def extract_enum(self, ast_enum: Dict) -> SyntaxElement:
        name: str = str(ast_enum.get("name", ""))  # 直接返回的不是 str
        content = [
            f"{value.get('name')} = {value.get('value')}"
            for value in ast_enum.get("values", {})
        ]
        return SyntaxElement(SyntaxType.ENUM, name, content)

    def extract_define(self, ast_define: str) -> SyntaxElement:
        # 处理 define 为空
        is_empty = False
        if " " not in ast_define:
            ast_define = ast_define + " "
            is_empty = True

        cleaned_define = combine_splited_line(ast_define)
        name_match = re.match(r"(.*?\)) ", cleaned_define) or re.match(
            r"(.*?) ", ast_define
        )
        if not name_match:
            msg = f"Failed to extract define: {cleaned_define}"
            logger.error(msg)
            raise ValueError(msg)

        name = name_match.group(1)
        content = [cleaned_define[len(name) :].strip()]
        if is_empty:
            content = []  # define 为空
        return SyntaxElement(SyntaxType.DEFINE, name, content)

    def extract_variable(self, ast_variable: Dict) -> SyntaxElement:
        def variable_content(line_number: int) -> str:
            lines = []
            for line in self.lines[line_number - 1 :]:
                lines.append(line)
                if line.strip().endswith(";"):
                    break
            return combine_splited_line("".join(lines)).strip()

        name: str = str(ast_variable.get("name", ""))  # 直接返回的不是 str
        line_number = ast_variable.get("line_number")
        if not line_number:
            msg = f"Not found line number of variable: {name}."
            logger.error(msg)
            raise ValueError(msg)
        content = [variable_content(line_number)]
        logger.debug(f"Extracted variable: {name}")
        return SyntaxElement(SyntaxType.VARIABLE, name, content)

    def extract_struct(self, ast_class: Dict) -> SyntaxElement:
        def struct_content(line_number: int) -> List[str]:
            lines = []
            in_brace = 0
            for line in self.lines[line_number - 1 :]:
                for cha in line:
                    if cha == "{":
                        in_brace += 1
                    elif cha == "}":
                        in_brace -= 1
                lines.append(line)
                if in_brace == 0 and line.strip().endswith(";"):
                    break

            return lines

        name: str = str(ast_class.get("name", ""))  # 直接返回的不是 str
        line_number = ast_class.get("line_number")
        if not line_number:
            msg = f"Not found line number of struct: {name}."
            logger.error(msg)
            raise ValueError(msg)
        content = struct_content(line_number)
        logger.debug(f"Extracted struct: {name}")
        return SyntaxElement(SyntaxType.STRUCT, name, content)


if __name__ == "__main__":
    fn = "./tests/fixtures/sample_normalized.h"
    fn_json = "./tests/fixtures/parsed_sample_normalized.json"
    parser = HeaderFileParser(fn)
    print(parser.parse())
    parser.to_json(fn_json)
