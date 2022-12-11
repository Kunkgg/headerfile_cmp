import json
import logging
import pathlib
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from functools import cached_property
from typing import Dict, List

import CppHeaderParser

from common.utils import readlines
from headerfile.formatter import combine_splited_line

logger = logging.getLogger(__name__)


class CppSyntaxType(Enum):
    INCLUDE = "include"
    DEFINE = "define"
    ENUM = "enum"
    VARIABLE = "variable"
    STRUCT = "struct"


@dataclass(unsafe_hash=True)
class SyntaxElement:
    syntax_type: CppSyntaxType = field(hash=False)
    name: str
    content: List[str] = field(repr=False, hash=False)


@dataclass
class SyntaxElementCollection:
    elements: List[SyntaxElement] = field(default_factory=list)

    def __sub__(self, other):
        self_only_set = set(self) - set(other)
        return [element for element in self.elements if element.name in self_only_set]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.elements):
            res = self.elements[self.n].name
            self.n += 1
            return res
        else:
            raise StopIteration

    def intersection_names(self, other) -> List[str]:
        other_name_set = set(other)
        return [
            element.name for element in self.elements if element.name in other_name_set
        ]

    def intersection(self, other) -> List[Dict]:
        res = []
        for name in self.intersection_names(other):
            self_element = self.find_element_by_name(name)
            other_element = other.find_element_by_name(name)
            d = {**self_element.__dict__}
            d["other_content"] = other_element.content
            res.append(d)
        return res

    def find_element_by_name(self, name):
        for element in self.elements:
            if element.name == name:
                return element


@dataclass(frozen=True)
class ParsedHeaderFile:
    file: str = field(compare=False)
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

    def to_dict(self):
        return asdict(self)

    def to_json(self, fn, encoding='utf-8'):
        class ParsedHeaderFileJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, CppSyntaxType):
                    return obj.value
                return json.JSONEncoder.default(self, obj)

        with open(fn, "w", encoding=encoding) as fp:
            json.dump(self.to_dict(), fp, indent=2, cls=ParsedHeaderFileJSONEncoder)
        logger.info(f"Dumped ParsedHeaderFile to: {fn}")

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
        return self.parse().to_dict()

    def to_json(self, fn: str, encoding: str = "utf-8"):
        return self.parse().to_json(fn, encoding)

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
            SyntaxElement(CppSyntaxType.INCLUDE, include, [])
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
        # 将 CppHeaderParser 对象转化为字符串
        name: str = str(ast_enum.get("name", ""))
        content = [
            f"{value.get('name')} = {value.get('value')}"
            for value in ast_enum.get("values", {})
        ]
        return SyntaxElement(CppSyntaxType.ENUM, name, content)

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
        return SyntaxElement(CppSyntaxType.DEFINE, name, content)

    def extract_variable(self, ast_variable: Dict) -> SyntaxElement:
        def variable_content(line_number: int) -> str:
            lines = []
            for line in self.lines[line_number - 1 :]:
                lines.append(line)
                if line.strip().endswith(";"):
                    break
            return combine_splited_line("".join(lines)).strip()

        # 将 CppHeaderParser 对象转化为字符串
        name: str = str(ast_variable.get("name", ""))
        line_number = ast_variable.get("line_number")
        if not line_number:
            msg = f"Not found line number of variable: {name}."
            logger.error(msg)
            raise ValueError(msg)
        content = [variable_content(line_number)]
        logger.debug(f"Extracted variable: {name}")
        return SyntaxElement(CppSyntaxType.VARIABLE, name, content)

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

        # 将 CppHeaderParser 对象转化为字符串
        name: str = str(ast_class.get("name", ""))
        line_number = ast_class.get("line_number")
        if not line_number:
            msg = f"Not found line number of struct: {name}."
            logger.error(msg)
            raise ValueError(msg)
        content = struct_content(line_number)
        logger.debug(f"Extracted struct: {name}")
        return SyntaxElement(CppSyntaxType.STRUCT, name, content)
