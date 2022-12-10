import unittest

from headerfile_comparator import HeaderFileComparator

from prepare import prepare_parser_sample
from prepare import prepare_comparator_sample
from prepare import prepare_comparator_sample_seq_inner


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
        subdir = "sample_includes"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertTrue(cmptor_cp.cmp_includes.is_same)
        self.assertFalse(cmptor_modi.cmp_includes.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_includes.is_same)
        self.assertFalse(cmptor_modi_add.cmp_includes.is_same)
        self.assertFalse(cmptor_modi_del.cmp_includes.is_same)

    def test_cmp_defines(self):
        subdir = "sample_defines"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertTrue(cmptor_cp.cmp_defines.is_same)
        self.assertFalse(cmptor_modi.cmp_defines.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_defines.is_same)
        self.assertFalse(cmptor_modi_add.cmp_defines.is_same)
        self.assertFalse(cmptor_modi_del.cmp_defines.is_same)

    def test_cmp_enums(self):
        subdir = "sample_enums"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        cmptor_modi_seq_inner = prepare_comparator_sample_seq_inner(subdir)

        self.assertTrue(cmptor_cp.cmp_enums.is_same)
        self.assertFalse(cmptor_modi.cmp_enums.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_enums.is_same)
        self.assertFalse(cmptor_modi_seq_inner.cmp_enums.is_same)
        self.assertFalse(cmptor_modi_add.cmp_enums.is_same)
        self.assertFalse(cmptor_modi_del.cmp_enums.is_same)

    def test_cmp_variables(self):
        subdir = "sample_variables"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertTrue(cmptor_cp.cmp_variables.is_same)
        self.assertFalse(cmptor_modi.cmp_variables.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_variables.is_same)
        self.assertFalse(cmptor_modi_add.cmp_variables.is_same)
        self.assertFalse(cmptor_modi_del.cmp_variables.is_same)

    def test_cmp_structs(self):
        subdir = "sample_structs"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        cmptor_modi_seq_inner = prepare_comparator_sample_seq_inner(subdir)

        self.assertTrue(cmptor_cp.cmp_structs.is_same)
        self.assertFalse(cmptor_modi.cmp_structs.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_seq_inner.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_add.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_del.cmp_structs.is_same)

