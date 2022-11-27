import unittest
from headerfile_comparator import HeaderFileComparator


class TestHeaderFileComparator(unittest.TestCase):
    def test_is_same(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmp_copy = HeaderFileComparator(fn, fn_copy)
        cmp_modified = HeaderFileComparator(fn, fn_modified)
        self.assertTrue(cmp_copy.is_same)
        self.assertFalse(cmp_modified.is_same)

    def test_text_cmp(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmp_copy = HeaderFileComparator(fn, fn_copy)
        cmp_modified = HeaderFileComparator(fn, fn_modified)
        cmp_copy_text_diff = cmp_copy.text_cmp().get('text_diff')
        cmp_modified_text_diff = cmp_modified.text_cmp().get('text_diff')
        self.assertEqual(cmp_copy_text_diff, "")
        self.assertNotEqual(cmp_modified_text_diff, "")
