#ifndef Py_AST_H
#define Py_AST_H
#ifdef __cplusplus
extern "C" {
#endif

PyAPI_FUNC(int) PyAST_Validate(mod_ty);
PyAPI_FUNC(mod_ty) PyAST_FromNode(
    const node *n,
    PyCompilerFlags *flags,
    const char *filename,       /* decoded from the filesystem encoding */
    PyArena *arena);
PyAPI_FUNC(mod_ty) PyAST_FromNodeObject(
    const node *n,
    PyCompilerFlags *flags,
    PyObject *filename,
    PyArena *arena);

#ifndef Py_LIMITED_API

/* _PyAST_ExprAsUnicode is defined in ast_unparse.c */
PyAPI_FUNC(PyObject *) _PyAST_ExprAsUnicode(expr_ty);

/* Return the borrowed reference to the first literal string in the
   sequence of statemnts or NULL if it doesn't start from a literal string.
   Doesn't set exception. */
PyAPI_FUNC(PyObject *) _PyAST_GetDocString(asdl_seq *);

#endif /* !Py_LIMITED_API */

#ifdef __cplusplus
}
#endif
#endif /* !Py_AST_H */

#ifndef Py_CPYTHON_UNICODEOBJECT_H
#  error "this header file must not be included directly"
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* Py_UNICODE was the native Unicode storage format (code unit) used by
   Python and represents a single Unicode element in the Unicode type.
   With PEP 393, Py_UNICODE is deprecated and replaced with a
   typedef to wchar_t. */
#define PY_UNICODE_TYPE wchar_t
/* Py_DEPRECATED(3.3) */ typedef wchar_t Py_UNICODE;

/* --- Internal Unicode Operations ---------------------------------------- */

/* Since splitting on whitespace is an important use case, and
   whitespace in most situations is solely ASCII whitespace, we
   optimize for the common case by using a quick look-up table
   _Py_ascii_whitespace (see below) with an inlined check.

 */
#define Py_UNICODE_ISSPACE(ch) \
    ((ch) < 128U ? _Py_ascii_whitespace[(ch)] : _PyUnicode_IsWhitespace(ch))

/* ! modified sequence */
#define Py_UNICODE_ISLINEBREAK(ch) _PyUnicode_IsLinebreak(ch)
#define Py_UNICODE_ISLOWER(ch) _PyUnicode_IsLowercase(ch)
#define Py_UNICODE_ISUPPER(ch) _PyUnicode_IsUppercase(ch)
#define Py_UNICODE_ISTITLE(ch) _PyUnicode_IsTitlecase(ch)

/* ! modified sequence */
#define Py_UNICODE_TOTITLE(ch) _PyUnicode_ToTitlecase(ch)
#define Py_UNICODE_TOUPPER(ch) _PyUnicode_ToUppercase(ch)
#define Py_UNICODE_TOLOWER(ch) _PyUnicode_ToLowercase(ch)

#define Py_UNICODE_ISDECIMAL(ch) _PyUnicode_IsDecimalDigit(ch)
#define Py_UNICODE_ISDIGIT(ch) _PyUnicode_IsDigit(ch)
#define Py_UNICODE_ISNUMERIC(ch) _PyUnicode_IsNumeric(ch)
#define Py_UNICODE_ISPRINTABLE(ch) _PyUnicode_IsPrintable(ch)

#define Py_UNICODE_TODECIMAL(ch) _PyUnicode_ToDecimalDigit(ch)
#define Py_UNICODE_TODIGIT(ch) _PyUnicode_ToDigit(ch)
#define Py_UNICODE_TONUMERIC(ch) _PyUnicode_ToNumeric(ch)

#define Py_UNICODE_ISALPHA(ch) _PyUnicode_IsAlpha(ch)

#define Py_UNICODE_ISALNUM(ch) \
       (Py_UNICODE_ISALPHA(ch) || \
    Py_UNICODE_ISDECIMAL(ch) || \
    Py_UNICODE_ISDIGIT(ch) || \
    Py_UNICODE_ISNUMERIC(ch))

#define Py_UNICODE_COPY(target, source, length) \
    memcpy((target), (source), (length)*sizeof(Py_UNICODE))

#define Py_UNICODE_FILL(target, value, length) \
    do {Py_ssize_t i_; Py_UNICODE *t_ = (target); Py_UNICODE v_ = (value);\
        for (i_ = 0; i_ < (length); i_++) t_[i_] = v_;\
    } while (0)

/* macros to work with surrogates */
#define Py_UNICODE_IS_SURROGATE(ch) (0xD800 <= (ch) && (ch) <= 0xDFFF)
#define Py_UNICODE_IS_HIGH_SURROGATE(ch) (0xD800 <= (ch) && (ch) <= 0xDBFF)
#define Py_UNICODE_IS_LOW_SURROGATE(ch) (0xDC00 <= (ch) && (ch) <= 0xDFFF)
/* Join two surrogate characters and return a single Py_UCS4 value. */
#define Py_UNICODE_JOIN_SURROGATES(high, low)  \
    (((((Py_UCS4)(high) & 0x03FF) << 10) |      \
      ((Py_UCS4)(low) & 0x03FF)) + 0x10000)
/* high surrogate = top 10 bits added to D800 */
#define Py_UNICODE_HIGH_SURROGATE(ch) (0xD800 - (0x10000 >> 10) + ((ch) >> 10))

/* Check if substring matches at given offset.  The offset must be
   valid, and the substring must not be empty. */

#define Py_UNICODE_MATCH(string, offset, substring) \
    ((*((string)->wstr + (offset)) == *((substring)->wstr)) && \
     ((*((string)->wstr + (offset) + (substring)->wstr_length-1) == *((substring)->wstr + (substring)->wstr_length-1))) && \
     !memcmp((string)->wstr + (offset), (substring)->wstr, (substring)->wstr_length*sizeof(Py_UNICODE)))

/* low surrogate = bottom 10 bits added to DC00 */
#define Py_UNICODE_LOW_SURROGATE(ch) (0xDC00 + ((ch) & 0x3FF))