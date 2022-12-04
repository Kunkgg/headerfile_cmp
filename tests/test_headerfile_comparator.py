import unittest

from headerfile_comparator import HeaderFileComparator
from headerfile_parser import HeaderFileParser

from prepare import prepare_parser_sample


class TestHeaderFileComparator(unittest.TestCase):
    def setUp(self) -> None:
        fn = "ast.h"
        fn_cp = "ast_copy.h"
        fn_modi = "ast_modified.h"
        self.parsed = prepare_parser_sample(fn).parse()
        self.parsed_cp = prepare_parser_sample(fn_cp).parse()
        self.parsed_modi = prepare_parser_sample(fn_modi).parse()

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

    def test_cmp_includes(self):
        cmptor_cp = HeaderFileComparator(self.parsed, self.parsed_cp)
        cmptor_modi = HeaderFileComparator(self.parsed, self.parsed_modi)
        # cmp1 = cmptor_cp.cmp_includes
        # self.assertEqual(cmptor_cp.cmp_includes.is_same)
        # self.assertTrue(cmptor_cp.cmp_includes.is_same)
        self.assertFalse(cmptor_modi.cmp_includes.is_same)