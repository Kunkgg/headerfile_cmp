#ifndef Py_AST_H
#define Py_AST_H
#ifdef __cplusplus
extern "C" {
#endif
PyAPI_FUNC(int) PyAST_Validate(mod_ty);
PyAPI_FUNC(mod_ty) PyAST_FromNode(const node *n, PyCompilerFlags *flags,
                                  const char *filename, PyArena *arena);
PyAPI_FUNC(mod_ty) PyAST_FromNodeObject(const node *n, PyCompilerFlags *flags,
                                        PyObject *filename, PyArena *arena);
#ifndef Py_LIMITED_API
PyAPI_FUNC(PyObject *) _PyAST_ExprAsUnicode(expr_ty);
PyAPI_FUNC(PyObject *) _PyAST_GetDocString(asdl_seq *);
#endif
#ifdef __cplusplus
}
#endif
#endif
#ifndef Py_CPYTHON_UNICODEOBJECT_H
#error "this header file must not be included directly"
#endif
#ifdef __cplusplus
extern "C" {
#endif
#define PY_UNICODE_TYPE wchar_t
typedef wchar_t Py_UNICODE;
#define Py_UNICODE_ISSPACE(ch)                                                 \
  ((ch) < 128U ? _Py_ascii_whitespace[(ch)] : _PyUnicode_IsWhitespace(ch))
#define Py_UNICODE_ISLOWER(ch) _PyUnicode_IsLowercase(ch)
#define Py_UNICODE_ISUPPER(ch) _PyUnicode_IsUppercase(ch)
#define Py_UNICODE_ISTITLE(ch) _PyUnicode_IsTitlecase(ch)
#define Py_UNICODE_ISLINEBREAK(ch) _PyUnicode_IsLinebreak(ch)
#define Py_UNICODE_TOLOWER(ch) _PyUnicode_ToLowercase(ch)
#define Py_UNICODE_TOUPPER(ch) _PyUnicode_ToUppercase(ch)
#define Py_UNICODE_TOTITLE(ch) _PyUnicode_ToTitlecase(ch)
#define Py_UNICODE_ISDECIMAL(ch) _PyUnicode_IsDecimalDigit(ch)
#define Py_UNICODE_ISDIGIT(ch) _PyUnicode_IsDigit(ch)
#define Py_UNICODE_ISNUMERIC(ch) _PyUnicode_IsNumeric(ch)
#define Py_UNICODE_ISPRINTABLE(ch) _PyUnicode_IsPrintable(ch)
#define Py_UNICODE_TODECIMAL(ch) _PyUnicode_ToDecimalDigit(ch)
#define Py_UNICODE_TODIGIT(ch) _PyUnicode_ToDigit(ch)
#define Py_UNICODE_TONUMERIC(ch) _PyUnicode_ToNumeric(ch)
#define Py_UNICODE_ISALPHA(ch) _PyUnicode_IsAlpha(ch)
#define Py_UNICODE_ISALNUM(ch)                                                 \
  (Py_UNICODE_ISALPHA(ch) || Py_UNICODE_ISDECIMAL(ch) ||                       \
   Py_UNICODE_ISDIGIT(ch) || Py_UNICODE_ISNUMERIC(ch))
#define Py_UNICODE_COPY(target, source, length)                                \
  memcpy((target), (source), (length) * sizeof(Py_UNICODE))
#define Py_UNICODE_FILL(target, value, length)                                 \
  do {                                                                         \
    Py_ssize_t i_;                                                             \
    Py_UNICODE *t_ = (target);                                                 \
    Py_UNICODE v_ = (value);                                                   \
    for (i_ = 0; i_ <= (length); i_++)                                         \
      t_[i_] = v_;                                                             \
  } while (0)
#define Py_UNICODE_IS_SURROGATE(ch) (0xD800 <= (ch) && (ch) <= 0xDFFF)
#define Py_UNICODE_IS_HIGH_SURROGATE(ch) (0xD800 <= (ch) && (ch) <= 0xDBFF)
#define Py_UNICODE_IS_LOW_SURROGATE(ch) (0xDC00 <= (ch) && (ch) <= 0xDFFF)
#define Py_UNICODE_JOIN_SURROGATES(high, low)                                  \
  (((((Py_UCS4)(high)&0x03FF) << 10) | ((Py_UCS4)(low)&0x03FF)) + 0x10000)
#define Py_UNICODE_HIGH_SURROGATE(ch) (0xD800 - (0x10000 >> 10) + ((ch) >> 10))
#define Py_UNICODE_LOW_SURROGATE(ch) (0xDC00 + ((ch)&0x3FF))
#define Py_UNICODE_MATCH(string, offset, substring)                            \
  ((*((string)->wstr + (offset)) == *((substring)->wstr)) &&                   \
   ((*((string)->wstr + (offset) + (substring)->wstr_length - 1) ==            \
     *((substring)->wstr + (substring)->wstr_length - 1))) &&                  \
   !memcmp((string)->wstr + (offset), (substring)->wstr,                       \
           (substring)->wstr_length * sizeof(Py_UNICODE)))
