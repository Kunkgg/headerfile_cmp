import difflib
import filecmp
import logging
import pathlib
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List

import common.init_log
from common.utils import readlines
from headerfile_parser import ParsedHeaderFile, SyntaxType

logger = logging.getLogger(__name__)


@dataclass
class ComparedSyntaxElement:
    name: str
    from_content: List[str] = field(repr=False)
    to_content: List[str] = field(repr=False)
    from_desc: str
    to_desc: str
    differ: difflib.HtmlDiff
    is_same: bool = field(init=False)
    diff_html: str = field(init=False, repr=False)

    def __post_init__(self):
        self.is_same = True if self.from_content == self.to_content else False
        self.diff_html = self.differ.make_table(
            self.from_content, self.to_content, self.from_desc, self.to_desc
        )


@dataclass
class ComparedSyntaxElementCollection:
    SyntaxType: SyntaxType
    from_onlys: List = field(default_factory=list)
    to_onlys: List = field(default_factory=list)
    commons: List[ComparedSyntaxElement] = field(default_factory=list)
    is_same: bool = field(init=False)
    diff_count: int = field(init=False)
    common_diffs: List[ComparedSyntaxElement] = field(init=False)

    def __post_init__(self):
        self.common_diffs = [
            common_compared
            for common_compared in self.commons
            if not common_compared.is_same
        ]
        self.diff_count = (
            len(self.from_onlys) + len(self.to_onlys) + len(self.common_diffs)
        )
        self.is_same = True if self.diff_count == 0 else False


class HeaderFileComparator:
    def __init__(
        self,
        from_: ParsedHeaderFile,
        to_: ParsedHeaderFile,
        from_desc: str = "from",
        to_desc: str = "to",
        differ=difflib.HtmlDiff(),
    ):
        self.from_ = from_
        self.to_ = to_
        self.from_desc = from_desc
        self.to_desc = to_desc
        self.differ = differ
        self.from_fn = pathlib.Path(self.from_.file).name
        self.to_fn = pathlib.Path(self.to_.file).name

    def compare(self):
        pass

    @cached_property
    def is_text_same(self):
        return filecmp.cmp(self.from_.file, self.to_.file)

    @cached_property
    def is_interface_same(self):
        pass
        # return self.from_ == self.to_

    @cached_property
    def from_lines(self):
        return readlines(self.from_.file)

    @cached_property
    def to_lines(self):
        return readlines(self.to_.file)

    def make_from_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.from_desc] + desc_parts)

    def make_to_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.to_desc] + desc_parts)

    @cached_property
    def cmp_text(self):
        from_desc = self.make_from_desc([self.from_fn])
        to_desc = self.make_to_desc([self.to_fn])
        return ComparedSyntaxElement(
            name="__text__",
            from_content=self.from_lines,
            to_content=self.to_lines,
            from_desc=from_desc,
            to_desc=to_desc,
            differ=self.differ,
        )

    def cmp_includes(self) -> ComparedSyntaxElementCollection:
        from_desc = self.make_from_desc([self.from_fn, "include"])
        to_desc = self.make_to_desc([self.to_fn, "include"])
        pass

        # from_includes_set = set(self.from_ast.includes)
        # to_includes_set = set(self.to_ast.includes)
        # if from_includes_set == to_includes_set:
        #     res.is_same = True
        #     res.diff_count = 0
        # else:
        #     from_only = list(from_includes_set - to_includes_set)
        #     to_only = list(to_includes_set - from_includes_set)
        #     res.from_only = from_only
        #     res.to_only = to_only
        #     res.diff_count = len(from_only) + len(to_only)

        # return res

    # def cmp_defines(self):
    # res = {
    #     "diff_count": 5,
    #     "from_only": ["std_only_defin_test1", "std_only_defin_test2"],
    #     "to_only": ["dev_only_defin_test1", "dev_only_defin_test2"],
    #     "diffs": [{"name": "define_diff_test1", "diff_html": ""}],
    # }

    # res = {
    #     "diff_count": 0,
    #     "from_only": [],
    #     "to_only": [],
    #     "diffs": [],
    # }
    # if self.is_text_same:
    #     return res

    # def cmp_enums(self):
    #     res = SyntaxElementCmpResult()

    #     pass

    # def cmp_variables(self):
    #     pass

    # def cmp_structs(self):
    #     pass
