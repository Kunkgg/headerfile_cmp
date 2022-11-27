import unittest
import json

import CppHeaderParser

from headerfile_comparator import HeaderFileComparator
from headerfile_formatter import normalize_clike
class TestHeaderFileComparator(unittest.TestCase):
    def test_is_same(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmptor_copy = HeaderFileComparator(fn, fn_copy)
        cmptor_modified = HeaderFileComparator(fn, fn_modified)
        self.assertTrue(cmptor_copy.is_text_same)
        self.assertFalse(cmptor_modified.is_text_same)

    def test_text_cmp(self):
        fn = "./tests/fixtures/ast.h"
        fn_copy = "./tests/fixtures/ast_copy.h"
        fn_modified = "./tests/fixtures/ast_modified.h"
        cmptor_copy = HeaderFileComparator(fn, fn_copy)
        cmptor_modified = HeaderFileComparator(fn, fn_modified)
        cmptor_copy_text_diff = cmptor_copy.cmp_text().diffs[0]
        cmptor_modified_text_diff = cmptor_modified.cmp_text().diffs[0]
        self.assertEqual(cmptor_copy_text_diff, "")
        self.assertNotEqual(cmptor_modified_text_diff, "")

    def test_include_cmp(self):
        fn = "./tests/fixtures/ast.h"
        fn_1 = "./tests/fixtures/ast_include_1.h"
        fn_2 = "./tests/fixtures/ast_include_2.h"
        fn_3 = "./tests/fixtures/ast_include_3.h"
        cmptor_1 = HeaderFileComparator(fn, fn_1)
        cmptor_2 = HeaderFileComparator(fn, fn_2)
        cmptor_3 = HeaderFileComparator(fn, fn_3)
        breakpoint()
        self.assertTrue(cmptor_1.cmp_include().is_same)
        self.assertFalse(cmptor_2.cmp_include().is_same)
        self.assertFalse(cmptor_3.cmp_include().is_same)

    def test_cppheader_parser(self):
        fn = "./tests/fixtures/sample.h"
        fn_normalized = "./tests/fixtures/sample_normalized.h"
        # json_normalized = "./tests/fixtures/sample_normalized.json"
        normalize_clike(fn, fn_normalized)
        header = CppHeaderParser.CppHeader(fn_normalized)
        # with open(json_normalized, 'w') as fp:
        #     fp.write(header.toJSON())
        self.assertIsInstance(header.includes, list)