import difflib
import filecmp
import logging
from functools import cached_property
from typing import Dict

import common.init_log
from common.utils import readlines

logger = logging.getLogger(__name__)


class HeaderFileComparator:
    def __init__(self, from_fn, to_fn, from_desc='from', to_desc='to'):
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

    def text_cmp(self) -> Dict:
        text_diff = (
            ""
            if self.is_same
            else self.differ.make_table(
                self.from_lines, self.to_lines, self.from_desc, self.to_desc
            )
        )

        return {"is_same": self.is_same, "text_diff": text_diff}

    def define_cmp(self):
        pass

    def enum_cmp(self):
        pass

    def variable_cmp(self):
        pass

    def struct_cmp(self):
        pass
