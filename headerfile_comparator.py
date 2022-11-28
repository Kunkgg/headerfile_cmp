import difflib
import filecmp
import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List
import CppHeaderParser

import common.init_log
from common.utils import readlines

logger = logging.getLogger(__name__)


@dataclass
class SyntaxItem:
    name: str
    lines: str | List[str] | None


@dataclass
class DiffItem:
    name: str
    diff_html: str


@dataclass
class SyntaxElementCmpResult:
    is_same: bool = False
    diff_count: int = -1
    from_only: List = field(default_factory=list)
    to_only: List = field(default_factory=list)
    diffs: List[DiffItem | str] = field(default_factory=list)


def parse_enum(enum: Dict) -> SyntaxItem:
    name: str = enum.get("name", "")
    lines = [
        f"{value.get('name')} = {value.get('value')}" for value in enum.get("values", {})
    ]
    return SyntaxItem(name, lines)


class HeaderFileComparator:
    def __init__(
        self, from_fn: str, to_fn: str, from_desc: str = "from", to_desc: str = "to"
    ):
        self.from_fn = from_fn
        self.to_fn = to_fn
        self.from_desc = from_desc
        self.to_desc = to_desc
        self.differ = difflib.HtmlDiff()

    @cached_property
    def is_text_same(self):
        return filecmp.cmp(self.from_fn, self.to_fn)

    @cached_property
    def is_interface_same(self):
        if self.is_text_same:
            return True
        # return all(self.is_define_same and self.is_)

    @cached_property
    def from_lines(self) -> List[str]:
        return readlines(self.from_fn)

    @cached_property
    def to_lines(self) -> List[str]:
        return readlines(self.to_fn)

    @cached_property
    def from_ast(self):
        return CppHeaderParser.CppHeader(self.from_fn)

    @cached_property
    def to_ast(self):
        return CppHeaderParser.CppHeader(self.to_fn)

    @cached_property
    def from_ast_enums(self) -> List[SyntaxItem]:
        return [parse_enum(enum) for enum in self.from_ast.enums]

    @cached_property
    def to_ast_enums(self) -> List[SyntaxItem]:
        return [parse_enum(enum) for enum in self.to_ast.enums]

    def make_from_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.from_desc] + desc_parts)

    def make_to_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.to_desc] + desc_parts)

    def cmp_text(self) -> SyntaxElementCmpResult:
        text_from_desc = self.make_from_desc([self.from_fn])
        text_to_desc = self.make_to_desc([self.to_fn])

        text_diff = (
            ""
            if self.is_text_same
            else self.differ.make_table(
                self.from_lines, self.to_lines, text_from_desc, text_to_desc
            )
        )
        res = SyntaxElementCmpResult(is_same=self.is_text_same, diffs=[text_diff])

        return res

    def cmp_include(self) -> SyntaxElementCmpResult:
        res = SyntaxElementCmpResult()
        from_includes_set = set(self.from_ast.includes)
        to_includes_set = set(self.to_ast.includes)
        if from_includes_set == to_includes_set:
            res.is_same = True
            res.diff_count = 0
        else:
            from_only = list(from_includes_set - to_includes_set)
            to_only = list(to_includes_set - from_includes_set)
            res.from_only = from_only
            res.to_only = to_only
            res.diff_count = len(from_only) + len(to_only)

        return res

    def cmp_define(self):
        # res = {
        #     "diff_count": 5,
        #     "from_only": ["std_only_defin_test1", "std_only_defin_test2"],
        #     "to_only": ["dev_only_defin_test1", "dev_only_defin_test2"],
        #     "diffs": [{"name": "define_diff_test1", "diff_html": ""}],
        # }

        res = {
            "diff_count": 0,
            "from_only": [],
            "to_only": [],
            "diffs": [],
        }
        if self.is_text_same:
            return res

    def cmp_enum(self):
        res = SyntaxElementCmpResult()
        
        pass

    def cmp_variable(self):
        pass

    def cmp_struct(self):
        pass
