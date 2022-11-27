import difflib
import filecmp
import logging
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List

import common.init_log
from common.utils import readlines

logger = logging.getLogger(__name__)


@dataclass
class DiffItem:
    name: str
    diff_html: str


class HeaderFileComparator:
    def __init__(self, from_fn, to_fn, from_desc="from", to_desc="to"):
        self.from_fn = from_fn
        self.to_fn = to_fn
        self.from_desc = from_desc
        self.to_desc = to_desc
        self.differ = difflib.HtmlDiff()

    @cached_property
    def is_same(self):
        return filecmp.cmp(self.from_fn, self.to_fn)

    @cached_property
    def from_lines(self):
        return readlines(self.from_fn)

    @cached_property
    def to_lines(self):
        return readlines(self.to_fn)

    def make_from_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.from_desc] + desc_parts)

    def make_to_desc(self, desc_parts: List[str]) -> str:
        return "/".join([self.to_desc] + desc_parts)

    def cmp_text(self) -> Dict:
        text_from_desc = self.make_from_desc([self.from_fn])
        text_to_desc = self.make_to_desc([self.to_fn])

        text_diff = (
            ""
            if self.is_same
            else self.differ.make_table(
                self.from_lines, self.to_lines, text_from_desc, text_to_desc
            )
        )

        return {"is_same": self.is_same, "text_diff": text_diff}

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
        if self.is_same:
            return res

    def cmp_enum(self):
        pass

    def cmp_variable(self):
        pass

    def cmp_struct(self):
        pass

    def cmp_include(self):
        pass
