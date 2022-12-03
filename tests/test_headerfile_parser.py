import unittest
from headerfile_parser import HeaderFileParser
from headerfile_parser import SyntaxType


class TestHeaderFileParser(unittest.TestCase):
    def setUp(self) -> None:
        fn = "./tests/fixtures/sample_normalized.h"
        self.parser = HeaderFileParser(fn)

    def test_lines(self):
        lines = self.parser.lines
        self.assertIsInstance(lines[0], str)

    def test_includes(self):
        includes = self.parser.includes
        element = includes.elements[0]
        self.assertEqual(element.syntaxType, SyntaxType.INCLUDE)
        self.assertIsInstance(element.name, str)
        self.assertIsNone(element.content)

    def test_extract_define_empty(self):
        define = "Py_AST_H"
        extracted_define = self.parser.extract_define(define)
        self.assertEqual(extracted_define.name, define)
        self.assertEqual(extracted_define.content, "")

    def test_extract_define_normal(self):
        define = "Py_UNICODE_ISLOWER(ch) _PyUnicode_IsLowercase(ch)"
        extracted_define = self.parser.extract_define(define)
        self.assertEqual(extracted_define.name, "Py_UNICODE_ISLOWER(ch)")
        self.assertEqual(extracted_define.content, "_PyUnicode_IsLowercase(ch)")

    def test_extract_define_long(self):
        define = "Py_UNICODE_ISSPACE(ch)                                                 \\\n  ((ch) < 128U ? _Py_ascii_whitespace[(ch)] : _PyUnicode_IsWhitespace(ch))"
        extracted_define = self.parser.extract_define(define)
        self.assertEqual(extracted_define.name, "Py_UNICODE_ISSPACE(ch)")
        self.assertEqual(
            extracted_define.content,
            "((ch) < 128U ? _Py_ascii_whitespace[(ch)] : _PyUnicode_IsWhitespace(ch))",
        )

    def test_extract_define_multi_args(self):
        define = "Py_UNICODE_COPY(target, source, length)                                \\\n  memcpy((target), (source), (length) * sizeof(Py_UNICODE))"
        extracted_define = self.parser.extract_define(define)
        self.assertEqual(
            extracted_define.name, "Py_UNICODE_COPY(target, source, length)"
        )
        self.assertEqual(
            extracted_define.content,
            "memcpy((target), (source), (length) * sizeof(Py_UNICODE))",
        )

    def test_extract_define_multi_lines(self):
        define = "PyUnicode_READ_CHAR(unicode, index)                                    \\\n  (assert(PyUnicode_Check(unicode)), assert(PyUnicode_IS_READY(unicode)),      \\\n   (Py_UCS4)(PyUnicode_KIND((unicode)) == PyUnicode_1BYTE_KIND                 \\\n                 ? ((const Py_UCS1 *)(PyUnicode_DATA((unicode))))[(index)]     \\\n                 : (PyUnicode_KIND((unicode)) == PyUnicode_2BYTE_KIND          \\\n                        ? ((const Py_UCS2 *)(PyUnicode_DATA(                   \\\n                              (unicode))))[(index)]                            \\\n                        : ((const Py_UCS4 *)(PyUnicode_DATA(                   \\\n                              (unicode))))[(index)])))"
        extracted_define = self.parser.extract_define(define)
        self.assertEqual(extracted_define.name, "PyUnicode_READ_CHAR(unicode, index)")
        self.assertEqual(
            extracted_define.content,
            "(assert(PyUnicode_Check(unicode)), assert(PyUnicode_IS_READY(unicode)), (Py_UCS4)(PyUnicode_KIND((unicode)) == PyUnicode_1BYTE_KIND ? ((const Py_UCS1 *)(PyUnicode_DATA((unicode))))[(index)] : (PyUnicode_KIND((unicode)) == PyUnicode_2BYTE_KIND ? ((const Py_UCS2 *)(PyUnicode_DATA( (unicode))))[(index)] : ((const Py_UCS4 *)(PyUnicode_DATA( (unicode))))[(index)])))",
        )

    def test_defines(self):
        defines = self.parser.defines
        element = defines.elements[0]
        self.assertEqual(element.syntaxType, SyntaxType.DEFINE)
        self.assertIsInstance(element.name, str)
        self.assertIsInstance(element.content, str)

    def test_enums(self):
        enums_ = self.parser.enums
        element = enums_.elements[0]
        self.assertEqual(element.syntaxType, SyntaxType.ENUM)
        self.assertIsInstance(element.name, str)
        self.assertIsInstance(element.content, list)

    def test_variables(self):
        variables = self.parser.variables
        element = variables.elements[0]
        self.assertEqual(element.syntaxType, SyntaxType.VARIABLE)
        self.assertIsInstance(element.name, str)
        self.assertIsInstance(element.content, str)

    def test_extract_variable_no_inited(self):
        # ! 依赖测试 sample 文件
        ast_variable = {
            "line_number": 4,
            "name": "test_var_int_empty",
        }
        extracted_variable = self.parser.extract_variable(ast_variable)
        variable_content = "int test_var_int_empty;"
        self.assertEqual(extracted_variable.name, ast_variable["name"])
        self.assertEqual(extracted_variable.content.strip(), variable_content)

    def test_extract_variable_inited(self):
        # ! 依赖测试 sample 文件
        ast_variable = {
            "line_number": 7,
            "name": "test_var_int",
        }
        extracted_variable = self.parser.extract_variable(ast_variable)
        variable_content = "int test_var_int = 10000;"
        self.assertEqual(extracted_variable.name, ast_variable["name"])
        self.assertEqual(extracted_variable.content.strip(), variable_content)

    def test_extract_variable_expr(self):
        # ! 依赖测试 sample 文件
        ast_variable = {
            "line_number": 8,
            "name": "test_var_int_expr",
        }
        extracted_variable = self.parser.extract_variable(ast_variable)
        variable_content = "int test_var_int_expr = test_var_int + 222;"
        self.assertEqual(extracted_variable.name, ast_variable["name"])
        self.assertEqual(extracted_variable.content.strip(), variable_content)

    def test_extract_variable_muti_in_oneline(self):
        # ! robotpy-cppheaderparser 解析多个变量在同一行声明的形式时，结果不准确
        # ! 依赖测试 sample 文件
        ast_variable = {
            "line_number": 11,
            "name": "testc",
        }
        extracted_variable = self.parser.extract_variable(ast_variable)
        variable_content = "char test_a, test_b, testc;"
        self.assertEqual(extracted_variable.name, ast_variable["name"])
        self.assertEqual(extracted_variable.content.strip(), variable_content)

    def test_extract_variable_muti_lines(self):
        # ! 依赖测试 sample 文件
        ast_variable = {
            "line_number": 13,
            "name": "xx",
        }
        extracted_variable = self.parser.extract_variable(ast_variable)
        variable_content = "int xx = 5 + 50 * 100 + 3600 * 24 + 3600 * 1 - 3600 * 1 + 3600 * 24 - 3600 * 24 + 7200 * 1 - 7200 * 1;"
        self.assertEqual(extracted_variable.name, ast_variable["name"])
        self.assertEqual(extracted_variable.content.strip(), variable_content)
