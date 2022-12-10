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
        fn = "sample_include.h"
        fn_cp = "sample_include_copy.h"
        fn_modi = "sample_include_modified.h"
        fn_modi_seq = "sample_include_modified_sequence.h"
        fn_modi_add = "sample_include_modified_add.h"
        fn_modi_del = "sample_include_modified_del.h"

        parsed = prepare_parser_sample(fn).parse()
        parsed_cp = prepare_parser_sample(fn_cp).parse()
        parsed_modi = prepare_parser_sample(fn_modi).parse()
        parsed_modi_seq = prepare_parser_sample(fn_modi_seq).parse()
        parsed_modi_add = prepare_parser_sample(fn_modi_add).parse()
        parsed_modi_del = prepare_parser_sample(fn_modi_del).parse()

        cmptor_cp = HeaderFileComparator(parsed, parsed_cp)
        cmptor_modi = HeaderFileComparator(parsed, parsed_modi)
        cmptor_modi_seq = HeaderFileComparator(parsed, parsed_modi_seq)
        cmptor_modi_add = HeaderFileComparator(parsed, parsed_modi_add)
        cmptor_modi_del = HeaderFileComparator(parsed, parsed_modi_del)

        self.assertTrue(cmptor_cp.cmp_includes.is_same)
        self.assertFalse(cmptor_modi.cmp_includes.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_includes.is_same)
        self.assertFalse(cmptor_modi_add.cmp_includes.is_same)
        self.assertFalse(cmptor_modi_del.cmp_includes.is_same)

    def test_cmp_defines(self):
        pass
