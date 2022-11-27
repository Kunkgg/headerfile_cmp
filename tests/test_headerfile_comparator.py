import unittest
from headerfile_comparator import HeaderFileComparator


class TestHeaderFileComparator(unittest.TestCase):
    def test_is_same(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmptor_copy = HeaderFileComparator(fn, fn_copy)
        cmptor_modified = HeaderFileComparator(fn, fn_modified)
        self.assertTrue(cmptor_copy.is_same)
        self.assertFalse(cmptor_modified.is_same)

    def test_text_cmp(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmptor_copy = HeaderFileComparator(fn, fn_copy)
        cmptor_modified = HeaderFileComparator(fn, fn_modified)
        cmptor_copy_text_diff = cmptor_copy.cmp_text().get('text_diff')
        cmptor_modified_text_diff = cmptor_modified.cmp_text().get('text_diff')
        self.assertEqual(cmptor_copy_text_diff, "")
        self.assertNotEqual(cmptor_modified_text_diff, "")
