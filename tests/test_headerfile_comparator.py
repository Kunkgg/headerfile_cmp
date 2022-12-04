import unittest
import json

import CppHeaderParser

from headerfile_comparator import HeaderFileComparator
from headerfile_parser import HeaderFileParser

class TestHeaderFileComparator(unittest.TestCase):
    def setUp(self) -> None:
        fn = "./tests/fixtures/ast.h"
        fn_cp = "./tests/fixtures/ast_copy.h"
        fn_modi = "./tests/fixtures/ast_modified.h"
        self.parsed = HeaderFileParser(fn).parse()
        self.parsed_cp = HeaderFileParser(fn_cp).parse()
        self.parsed_modi = HeaderFileParser(fn_modi).parse()

    def test_is_same(self):
        cmptor_cp = HeaderFileComparator(self.parsed, self.parsed_cp)
        cmptor_modi = HeaderFileComparator(self.parsed, self.parsed_modi)
        self.assertTrue(cmptor_cp.is_text_same)
        self.assertFalse(cmptor_modi.is_text_same)

    def test_cmp_text(self):
        cmptor_cp = HeaderFileComparator(self.parsed, self.parsed_cp)
        cmptor_modi = HeaderFileComparator(self.parsed, self.parsed_modi)
        self.assertEqual(cmptor_cp.cmp_text.name, "__text__")
        self.assertTrue(cmptor_cp.cmp_text.is_same)
        self.assertFalse(cmptor_modi.cmp_text.is_same)

    # def test_include_cmp(self):
    #     fn = "./tests/fixtures/ast.h"
    #     fn_1 = "./tests/fixtures/ast_include_1.h"
    #     fn_2 = "./tests/fixtures/ast_include_2.h"
    #     fn_3 = "./tests/fixtures/ast_include_3.h"
    #     cmptor_1 = HeaderFileComparator(fn, fn_1)
    #     cmptor_2 = HeaderFileComparator(fn, fn_2)
    #     cmptor_3 = HeaderFileComparator(fn, fn_3)
    #     cmpres_1 = cmptor_1.cmp_include()
    #     cmpres_2 = cmptor_2.cmp_include()
    #     cmpres_3 = cmptor_3.cmp_include()
    #     self.assertTrue(cmpres_1.is_same)
    #     self.assertFalse(cmpres_2.is_same)
    #     self.assertFalse(cmpres_3.is_same)
