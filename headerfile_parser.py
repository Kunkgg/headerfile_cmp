import logging
import re
from collections import namedtuple
from dataclasses import dataclass
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
    content: str | List[str] | None


@dataclass
class SyntaxElementCollection:
    elements: List[SyntaxElement]


class HeaderFileParser:
    def __init__(self, fn: str):
        self.fn = fn

    @cached_property
    def parse(self):
        pass

    @cached_property
    def lines(self) -> List[str]:
        return readlines(self.fn)

    @cached_property
    def includes(self) -> SyntaxElementCollection:
        extracted_includes = [
            SyntaxElement(SyntaxType.INCLUDE, include, None)
            for include in self._ast.includes
        ]
        logger.debug(f"Extracted includes: {len(extracted_includes)}")
        return SyntaxElementCollection(extracted_includes)

    @cached_property
    def defines(self):
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
        pass

    def to_json(self, fn: str, encoding: str = "utf-8"):
        pass

    @cached_property
    def _ast(self):
        logger.debug(f"Parsered {self.fn} by robotpy-cppheaderparser")
        return CppHeaderParser.CppHeader(self.fn)

    @staticmethod
    def extract_enum(ast_enum: Dict) -> SyntaxElement:
        name: str = ast_enum.get("name", "")
        content = [
            f"{value.get('name')} = {value.get('value')}"
            for value in ast_enum.get("values", {})
        ]
        return SyntaxElement(SyntaxType.ENUM, name, content)

    @staticmethod
    def extract_define(ast_define: str) -> SyntaxElement:
        # 处理 define 为空
        if " " not in ast_define:
            ast_define = ast_define + " "

        # 清理换行及连续 whitespace
        cleaned_define = combine_splited_line(ast_define)
        name_match = re.match(r"(.*?\)) ", cleaned_define) or re.match(
            r"(.*?) ", ast_define
        )
        if not name_match:
            msg = f"Failed to extract define: {cleaned_define}"
            logger.error(msg)
            raise ValueError(msg)

        name = name_match.group(1)
        content = cleaned_define[len(name) :].strip()
        return SyntaxElement(SyntaxType.DEFINE, name, content)

    @staticmethod
    def extract_variable(ast_variable: Dict) -> SyntaxElement:
        pass
    #     name: str = ast_variable.get("name", "")
    #     content = VariableContent(
    #         variableType,
    #     )
