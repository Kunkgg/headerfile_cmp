import unittest
import pathlib

from prepare import prepare_comparator_sample
from prepare import prepare_comparator_sample_seq_inner
from prepare import FIXTURES_PATH
from headerfile.parser import CppSyntaxType


class TestHeaderFileComparator(unittest.TestCase):
    def test_is_text_same(self):
        subdir = "sample_is_same"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertTrue(cmptor_cp.is_text_same)
        self.assertFalse(cmptor_modi.is_text_same)
        self.assertFalse(cmptor_modi_seq.is_text_same)
        self.assertFalse(cmptor_modi_add.is_text_same)
        self.assertFalse(cmptor_modi_del.is_text_same)

    def test_is_interface_same(self):
        subdir = "sample_is_same"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertTrue(cmptor_cp.is_interface_same)
        self.assertFalse(cmptor_modi.is_interface_same)
        self.assertTrue(cmptor_modi_seq.is_interface_same)
        self.assertFalse(cmptor_modi_add.is_interface_same)
        self.assertFalse(cmptor_modi_del.is_interface_same)

    def test_diff_count(self):
        subdir = "sample_is_same"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertEqual(cmptor_cp.diff_count, 0)
        self.assertGreater(cmptor_modi.diff_count, 0)
        self.assertEqual(cmptor_modi_seq.diff_count, 0)
        self.assertGreater(cmptor_modi_add.diff_count, 0)
        self.assertGreater(cmptor_modi_del.diff_count, 0)

    def test_cmp_text(self):
        subdir = "sample_is_same"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertEqual(cmptor_cp.cmp_text.name, "__text__")
        self.assertTrue(cmptor_cp.cmp_text.is_same)
        self.assertFalse(cmptor_modi.cmp_text.is_same)
        self.assertFalse(cmptor_modi_seq.cmp_text.is_same)
        self.assertFalse(cmptor_modi_add.cmp_text.is_same)
        self.assertFalse(cmptor_modi_del.cmp_text.is_same)

    def test_cmp_includes(self):
        subdir = "sample_includes"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        self.assertEqual(cmptor_cp.cmp_includes.syntax_type, CppSyntaxType.INCLUDE)
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

        self.assertEqual(cmptor_cp.cmp_defines.syntax_type, CppSyntaxType.DEFINE)
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

        self.assertEqual(cmptor_cp.cmp_enums.syntax_type, CppSyntaxType.ENUM)
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

        self.assertEqual(cmptor_cp.cmp_variables.syntax_type, CppSyntaxType.VARIABLE)
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

        self.assertEqual(cmptor_cp.cmp_structs.syntax_type, CppSyntaxType.STRUCT)
        self.assertTrue(cmptor_cp.cmp_structs.is_same)
        self.assertFalse(cmptor_modi.cmp_structs.is_same)
        self.assertTrue(cmptor_modi_seq.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_seq_inner.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_add.cmp_structs.is_same)
        self.assertFalse(cmptor_modi_del.cmp_structs.is_same)

    def test_to_json(self):
        subdir = "sample_is_same"
        (
            cmptor_cp,
            cmptor_modi,
            cmptor_modi_seq,
            cmptor_modi_add,
            cmptor_modi_del,
        ) = prepare_comparator_sample(subdir)

        subdir_path = FIXTURES_PATH / subdir

        fp_cp = subdir_path / 'compared_copy.json'
        fp_modi = subdir_path / 'compared_modified.json'
        fp_modi_seq = subdir_path / 'compared_modified_sequence.json'
        fp_modi_add = subdir_path / 'compared_modified_add.json'
        fp_modi_del = subdir_path / 'compared_modified_del.json'

        cmptor_cp.to_json(str(fp_cp))
        cmptor_modi.to_json(str(fp_modi))
        cmptor_modi_seq.to_json(str(fp_modi_seq))
        cmptor_modi_add.to_json(str(fp_modi_add))
        cmptor_modi_del.to_json(str(fp_modi_del))

        self.assertTrue(fp_cp.is_file())
        self.assertTrue(fp_modi.is_file())
        self.assertTrue(fp_modi_seq.is_file())
        self.assertTrue(fp_modi_add.is_file())
        self.assertTrue(fp_modi_del.is_file())
