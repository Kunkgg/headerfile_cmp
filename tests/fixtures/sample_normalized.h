#include "test-node1.h"
#include "test-node2.h"
#include "test-node3.h"
int test_var_int_empty;
float test_var_float_empty;
char test_var_char_empty;
int test_var_int = 10000;
int test_var_int_expr = test_var_int + 222;
int test_var_float = 3.14;
int test_var_char = 'aaa';
char test_a, test_b, testc;
int x = 5, y = 6, z = 50;
int xx = 5 + 50 * 100 + 3600 * 24 + 3600 * 1 - 3600 * 1 + 3600 * 24 -
         3600 * 24 + 7200 * 1 - 7200 * 1;
#ifndef Py_AST_H
#define Py_AST_H
#ifdef __cplusplus
extern "C" {
#endif
#include "Python-ast.h"
#include "node.h"
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
    for (i_ = 0; i_ < (length); i_++)                                          \
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
typedef struct {
  PyObject_HEAD Py_ssize_t length;
  Py_hash_t hash;
  struct {
    unsigned int interned : 2;
    unsigned int kind : 3;
    unsigned int compact : 1;
    unsigned int ascii : 1;
    unsigned int ready : 1;
    unsigned int : 24;
  } state;
  wchar_t *wstr;
} PyASCIIObject;
typedef struct {
  PyASCIIObject _base;
  Py_ssize_t utf8_length;
  char *utf8;
  Py_ssize_t wstr_length;
} PyCompactUnicodeObject;
typedef struct {
  PyCompactUnicodeObject _base;
  union {
    void *any;
    Py_UCS1 *latin1;
    Py_UCS2 *ucs2;
    Py_UCS4 *ucs4;
  } data;
} PyUnicodeObject;
#define PyUnicode_WSTR_LENGTH(op)                                              \
  (PyUnicode_IS_COMPACT_ASCII(op)                                              \
       ? ((PyASCIIObject *)op)->length                                         \
       : ((PyCompactUnicodeObject *)op)->wstr_length)
#define PyUnicode_GET_SIZE(op)                                                 \
  (assert(PyUnicode_Check(op)),                                                \
   (((PyASCIIObject *)(op))->wstr)                                             \
       ? PyUnicode_WSTR_LENGTH(op)                                             \
       : ((void)PyUnicode_AsUnicode(_PyObject_CAST(op)),                       \
          assert(((PyASCIIObject *)(op))->wstr), PyUnicode_WSTR_LENGTH(op)))
#define PyUnicode_GET_DATA_SIZE(op) (PyUnicode_GET_SIZE(op) * Py_UNICODE_SIZE)
#define PyUnicode_AS_UNICODE(op)                                               \
  (assert(PyUnicode_Check(op)), (((PyASCIIObject *)(op))->wstr)                \
                                    ? (((PyASCIIObject *)(op))->wstr)          \
                                    : PyUnicode_AsUnicode(_PyObject_CAST(op)))
#define PyUnicode_AS_DATA(op) ((const char *)(PyUnicode_AS_UNICODE(op)))
#define SSTATE_NOT_INTERNED 0
#define SSTATE_INTERNED_MORTAL 1
#define SSTATE_INTERNED_IMMORTAL 2
#define PyUnicode_IS_ASCII(op)                                                 \
  (assert(PyUnicode_Check(op)), assert(PyUnicode_IS_READY(op)),                \
   ((PyASCIIObject *)op)->state.ascii)
#define PyUnicode_IS_COMPACT(op) (((PyASCIIObject *)(op))->state.compact)
#define PyUnicode_IS_COMPACT_ASCII(op)                                         \
  (((PyASCIIObject *)op)->state.ascii && PyUnicode_IS_COMPACT(op))
enum PyUnicode_Kind {
  PyUnicode_WCHAR_KIND = 0,
  PyUnicode_1BYTE_KIND = 1,
  PyUnicode_2BYTE_KIND = 2,
  PyUnicode_4BYTE_KIND = 4
};
enum PyUnicode_Kind_AA {
  PyUnicode_WCHAR_KIND_AA = 0,
  PyUnicode_1BYTE_KIND_AA = 1,
  PyUnicode_2BYTE_KIND_AA = 2,
  PyUnicode_4BYTE_KIND_AA = 4
};
enum PyUnicode_Kind_BB {
  PyUnicode_WCHAR_KIND_BB = 0,
  PyUnicode_1BYTE_KIND_BB = 1,
  PyUnicode_2BYTE_KIND_BB = 2,
  PyUnicode_4BYTE_KIND_BB = 4
};
#define PyUnicode_1BYTE_DATA(op) ((Py_UCS1 *)PyUnicode_DATA(op))
#define PyUnicode_2BYTE_DATA(op) ((Py_UCS2 *)PyUnicode_DATA(op))
#define PyUnicode_4BYTE_DATA(op) ((Py_UCS4 *)PyUnicode_DATA(op))
#define PyUnicode_KIND(op)                                                     \
  (assert(PyUnicode_Check(op)), assert(PyUnicode_IS_READY(op)),                \
   ((PyASCIIObject *)(op))->state.kind)
#define _PyUnicode_COMPACT_DATA(op)                                            \
  (PyUnicode_IS_ASCII(op) ? ((void *)((PyASCIIObject *)(op) + 1))              \
                          : ((void *)((PyCompactUnicodeObject *)(op) + 1)))
#define _PyUnicode_NONCOMPACT_DATA(op)                                         \
  (assert(((PyUnicodeObject *)(op))->data.any),                                \
   ((((PyUnicodeObject *)(op))->data.any)))
#define PyUnicode_DATA(op)                                                     \
  (assert(PyUnicode_Check(op)), PyUnicode_IS_COMPACT(op)                       \
                                    ? _PyUnicode_COMPACT_DATA(op)              \
                                    : _PyUnicode_NONCOMPACT_DATA(op))
#define PyUnicode_WRITE(kind, data, index, value)                              \
  do {                                                                         \
    switch ((kind)) {                                                          \
    case PyUnicode_1BYTE_KIND: {                                               \
      ((Py_UCS1 *)(data))[(index)] = (Py_UCS1)(value);                         \
      break;                                                                   \
    }                                                                          \
    case PyUnicode_2BYTE_KIND: {                                               \
      ((Py_UCS2 *)(data))[(index)] = (Py_UCS2)(value);                         \
      break;                                                                   \
    }                                                                          \
    default: {                                                                 \
      assert((kind) == PyUnicode_4BYTE_KIND);                                  \
      ((Py_UCS4 *)(data))[(index)] = (Py_UCS4)(value);                         \
    }                                                                          \
    }                                                                          \
  } while (0)
#define PyUnicode_READ(kind, data, index)                                      \
  ((Py_UCS4)((kind) == PyUnicode_1BYTE_KIND                                    \
                 ? ((const Py_UCS1 *)(data))[(index)]                          \
                 : ((kind) == PyUnicode_2BYTE_KIND                             \
                        ? ((const Py_UCS2 *)(data))[(index)]                   \
                        : ((const Py_UCS4 *)(data))[(index)])))
#define PyUnicode_READ_CHAR(unicode, index)                                    \
  (assert(PyUnicode_Check(unicode)), assert(PyUnicode_IS_READY(unicode)),      \
   (Py_UCS4)(PyUnicode_KIND((unicode)) == PyUnicode_1BYTE_KIND                 \
                 ? ((const Py_UCS1 *)(PyUnicode_DATA((unicode))))[(index)]     \
                 : (PyUnicode_KIND((unicode)) == PyUnicode_2BYTE_KIND          \
                        ? ((const Py_UCS2 *)(PyUnicode_DATA(                   \
                              (unicode))))[(index)]                            \
                        : ((const Py_UCS4 *)(PyUnicode_DATA(                   \
                              (unicode))))[(index)])))
#define PyUnicode_GET_LENGTH(op)                                               \
  (assert(PyUnicode_Check(op)), assert(PyUnicode_IS_READY(op)),                \
   ((PyASCIIObject *)(op))->length)
#define PyUnicode_IS_READY(op) (((PyASCIIObject *)op)->state.ready)
#define PyUnicode_READY(op)                                                    \
  (assert(PyUnicode_Check(op)),                                                \
   (PyUnicode_IS_READY(op) ? 0 : _PyUnicode_Ready(_PyObject_CAST(op))))
#define PyUnicode_MAX_CHAR_VALUE(op)                                           \
  (assert(PyUnicode_IS_READY(op)),                                             \
   (PyUnicode_IS_ASCII(op)                                                     \
        ? (0x7f)                                                               \
        : (PyUnicode_KIND(op) == PyUnicode_1BYTE_KIND                          \
               ? (0xffU)                                                       \
               : (PyUnicode_KIND(op) == PyUnicode_2BYTE_KIND ? (0xffffU)       \
                                                             : (0x10ffffU)))))
PyAPI_FUNC(PyObject *) PyUnicode_New(Py_ssize_t size, Py_UCS4 maxchar);
PyAPI_FUNC(int) _PyUnicode_Ready(PyObject *unicode);
PyAPI_FUNC(PyObject *) _PyUnicode_Copy(PyObject *unicode);
PyAPI_FUNC(Py_ssize_t)
    PyUnicode_CopyCharacters(PyObject *to, Py_ssize_t to_start, PyObject *from,
                             Py_ssize_t from_start, Py_ssize_t how_many);
PyAPI_FUNC(void)
    _PyUnicode_FastCopyCharacters(PyObject *to, Py_ssize_t to_start,
                                  PyObject *from, Py_ssize_t from_start,
                                  Py_ssize_t how_many);
PyAPI_FUNC(Py_ssize_t) PyUnicode_Fill(PyObject *unicode, Py_ssize_t start,
                                      Py_ssize_t length, Py_UCS4 fill_char);
PyAPI_FUNC(void) _PyUnicode_FastFill(PyObject *unicode, Py_ssize_t start,
                                     Py_ssize_t length, Py_UCS4 fill_char);
PyAPI_FUNC(PyObject *)
    PyUnicode_FromUnicode(const Py_UNICODE *u, Py_ssize_t size);
PyAPI_FUNC(PyObject *)
    PyUnicode_FromKindAndData(int kind, const void *buffer, Py_ssize_t size);
PyAPI_FUNC(PyObject *)
    _PyUnicode_FromASCII(const char *buffer, Py_ssize_t size);
PyAPI_FUNC(Py_UCS4)
    _PyUnicode_FindMaxChar(PyObject *unicode, Py_ssize_t start, Py_ssize_t end);
PyAPI_FUNC(Py_UNICODE *) PyUnicode_AsUnicode(PyObject *unicode);
PyAPI_FUNC(const Py_UNICODE *) _PyUnicode_AsUnicode(PyObject *unicode);
PyAPI_FUNC(Py_UNICODE *)
    PyUnicode_AsUnicodeAndSize(PyObject *unicode, Py_ssize_t *size);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE) PyUnicode_GetMax(void);
typedef struct {
  PyObject *buffer;
  void *data;
  enum PyUnicode_Kind kind;
  Py_UCS4 maxchar;
  Py_ssize_t size;
  Py_ssize_t pos;
  Py_ssize_t min_length;
  Py_UCS4 min_char;
  unsigned char overallocate;
  unsigned char readonly;
} _PyUnicodeWriter;
PyAPI_FUNC(void) _PyUnicodeWriter_Init(_PyUnicodeWriter *writer);
#define _PyUnicodeWriter_Prepare(WRITER, LENGTH, MAXCHAR)                      \
  (((MAXCHAR) <= (WRITER)->maxchar &&                                          \
    (LENGTH) <= (WRITER)->size - (WRITER)->pos)                                \
       ? 0                                                                     \
       : (((LENGTH) == 0) ? 0                                                  \
                          : _PyUnicodeWriter_PrepareInternal(                  \
                                (WRITER), (LENGTH), (MAXCHAR))))
PyAPI_FUNC(int)
    _PyUnicodeWriter_PrepareInternal(_PyUnicodeWriter *writer,
                                     Py_ssize_t length, Py_UCS4 maxchar);
#define _PyUnicodeWriter_PrepareKind(WRITER, KIND)                             \
  (assert((KIND) != PyUnicode_WCHAR_KIND),                                     \
   (KIND) <= (WRITER)->kind                                                    \
       ? 0                                                                     \
       : _PyUnicodeWriter_PrepareKindInternal((WRITER), (KIND)))
PyAPI_FUNC(int) _PyUnicodeWriter_PrepareKindInternal(_PyUnicodeWriter *writer,
                                                     enum PyUnicode_Kind kind);
PyAPI_FUNC(int)
    _PyUnicodeWriter_WriteChar(_PyUnicodeWriter *writer, Py_UCS4 ch);
PyAPI_FUNC(int)
    _PyUnicodeWriter_WriteStr(_PyUnicodeWriter *writer, PyObject *str);
PyAPI_FUNC(int)
    _PyUnicodeWriter_WriteSubstring(_PyUnicodeWriter *writer, PyObject *str,
                                    Py_ssize_t start, Py_ssize_t end);
PyAPI_FUNC(int)
    _PyUnicodeWriter_WriteASCIIString(_PyUnicodeWriter *writer, const char *str,
                                      Py_ssize_t len);
PyAPI_FUNC(int)
    _PyUnicodeWriter_WriteLatin1String(_PyUnicodeWriter *writer,
                                       const char *str, Py_ssize_t len);
PyAPI_FUNC(PyObject *) _PyUnicodeWriter_Finish(_PyUnicodeWriter *writer);
PyAPI_FUNC(void) _PyUnicodeWriter_Dealloc(_PyUnicodeWriter *writer);
PyAPI_FUNC(int)
    _PyUnicode_FormatAdvancedWriter(_PyUnicodeWriter *writer, PyObject *obj,
                                    PyObject *format_spec, Py_ssize_t start,
                                    Py_ssize_t end);
#ifdef HAVE_WCHAR_H
PyAPI_FUNC(void *) _PyUnicode_AsKind(PyObject *s, unsigned int kind);
#endif
PyAPI_FUNC(const char *)
    PyUnicode_AsUTF8AndSize(PyObject *unicode, Py_ssize_t *size);
#define _PyUnicode_AsStringAndSize PyUnicode_AsUTF8AndSize
PyAPI_FUNC(const char *) PyUnicode_AsUTF8(PyObject *unicode);
#define _PyUnicode_AsString PyUnicode_AsUTF8
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_Encode(const Py_UNICODE *s, Py_ssize_t size, const char *encoding,
                     const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeUTF7(const Py_UNICODE *data, Py_ssize_t length,
                         int base64SetO, int base64WhiteSpace,
                         const char *errors);
PyAPI_FUNC(PyObject *)
    _PyUnicode_EncodeUTF7(PyObject *unicode, int base64SetO,
                          int base64WhiteSpace, const char *errors);
PyAPI_FUNC(PyObject *)
    _PyUnicode_AsUTF8String(PyObject *unicode, const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeUTF8(const Py_UNICODE *data, Py_ssize_t length,
                         const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeUTF32(const Py_UNICODE *data, Py_ssize_t length,
                          const char *errors, int byteorder);
PyAPI_FUNC(PyObject *)
    _PyUnicode_EncodeUTF32(PyObject *object, const char *errors, int byteorder);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeUTF16(const Py_UNICODE *data, Py_ssize_t length,
                          const char *errors, int byteorder);
PyAPI_FUNC(PyObject *)
    _PyUnicode_EncodeUTF16(PyObject *unicode, const char *errors,
                           int byteorder);
PyAPI_FUNC(PyObject *)
    _PyUnicode_DecodeUnicodeEscape(const char *string, Py_ssize_t length,
                                   const char *errors,
                                   const char **first_invalid_escape);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeUnicodeEscape(const Py_UNICODE *data, Py_ssize_t length);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeRawUnicodeEscape(const Py_UNICODE *data, Py_ssize_t length);
PyAPI_FUNC(PyObject *)
    _PyUnicode_AsLatin1String(PyObject *unicode, const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeLatin1(const Py_UNICODE *data, Py_ssize_t length,
                           const char *errors);
PyAPI_FUNC(PyObject *)
    _PyUnicode_AsASCIIString(PyObject *unicode, const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeASCII(const Py_UNICODE *data, Py_ssize_t length,
                          const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeCharmap(const Py_UNICODE *data, Py_ssize_t length,
                            PyObject *mapping, const char *errors);
PyAPI_FUNC(PyObject *)
    _PyUnicode_EncodeCharmap(PyObject *unicode, PyObject *mapping,
                             const char *errors);
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_TranslateCharmap(const Py_UNICODE *data, Py_ssize_t length,
                               PyObject *table, const char *errors);
#ifdef MS_WINDOWS
Py_DEPRECATED(3.3) PyAPI_FUNC(PyObject *)
    PyUnicode_EncodeMBCS(const Py_UNICODE *data, Py_ssize_t length,
                         const char *errors);
#endif
PyAPI_FUNC(int) PyUnicode_EncodeDecimal(Py_UNICODE *s, Py_ssize_t length,
                                        char *output, const char *errors);
PyAPI_FUNC(PyObject *)
    PyUnicode_TransformDecimalToASCII(Py_UNICODE *s, Py_ssize_t length);
PyAPI_FUNC(PyObject *)
    _PyUnicode_TransformDecimalAndSpaceToASCII(PyObject *unicode);
PyAPI_FUNC(PyObject *)
    _PyUnicode_JoinArray(PyObject *separator, PyObject *const *items,
                         Py_ssize_t seqlen);
PyAPI_FUNC(int)
    _PyUnicode_EqualToASCIIId(PyObject *left, _Py_Identifier *right);
PyAPI_FUNC(int)
    _PyUnicode_EqualToASCIIString(PyObject *left, const char *right);
PyAPI_FUNC(PyObject *)
    _PyUnicode_XStrip(PyObject *self, int striptype, PyObject *sepobj);
PyAPI_FUNC(Py_ssize_t) _PyUnicode_InsertThousandsGrouping(
    _PyUnicodeWriter *writer, Py_ssize_t n_buffer, PyObject *digits,
    Py_ssize_t d_pos, Py_ssize_t n_digits, Py_ssize_t min_width,
    const char *grouping, PyObject *thousands_sep, Py_UCS4 *maxchar);
PyAPI_DATA(const unsigned char) _Py_ascii_whitespace[];
PyAPI_FUNC(int) _PyUnicode_IsLowercase(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsUppercase(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsTitlecase(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsXidStart(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsXidContinue(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsWhitespace(const Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsLinebreak(const Py_UCS4 ch);
PyAPI_FUNC(Py_UCS4) _PyUnicode_ToLowercase(Py_UCS4 ch);
PyAPI_FUNC(Py_UCS4) _PyUnicode_ToUppercase(Py_UCS4 ch);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UCS4) _PyUnicode_ToTitlecase(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_ToLowerFull(Py_UCS4 ch, Py_UCS4 *res);
PyAPI_FUNC(int) _PyUnicode_ToTitleFull(Py_UCS4 ch, Py_UCS4 *res);
PyAPI_FUNC(int) _PyUnicode_ToUpperFull(Py_UCS4 ch, Py_UCS4 *res);
PyAPI_FUNC(int) _PyUnicode_ToFoldedFull(Py_UCS4 ch, Py_UCS4 *res);
PyAPI_FUNC(int) _PyUnicode_IsCaseIgnorable(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsCased(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_ToDecimalDigit(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_ToDigit(Py_UCS4 ch);
PyAPI_FUNC(double) _PyUnicode_ToNumeric(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsDecimalDigit(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsDigit(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsNumeric(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsPrintable(Py_UCS4 ch);
PyAPI_FUNC(int) _PyUnicode_IsAlpha(Py_UCS4 ch);
Py_DEPRECATED(3.3) PyAPI_FUNC(size_t) Py_UNICODE_strlen(const Py_UNICODE *u);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    Py_UNICODE_strcpy(Py_UNICODE *s1, const Py_UNICODE *s2);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    Py_UNICODE_strcat(Py_UNICODE *s1, const Py_UNICODE *s2);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    Py_UNICODE_strncpy(Py_UNICODE *s1, const Py_UNICODE *s2, size_t n);
Py_DEPRECATED(3.3) PyAPI_FUNC(int)
    Py_UNICODE_strcmp(const Py_UNICODE *s1, const Py_UNICODE *s2);
Py_DEPRECATED(3.3) PyAPI_FUNC(int)
    Py_UNICODE_strncmp(const Py_UNICODE *s1, const Py_UNICODE *s2, size_t n);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    Py_UNICODE_strchr(const Py_UNICODE *s, Py_UNICODE c);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    Py_UNICODE_strrchr(const Py_UNICODE *s, Py_UNICODE c);
PyAPI_FUNC(PyObject *) _PyUnicode_FormatLong(PyObject *, int, int, int);
Py_DEPRECATED(3.3) PyAPI_FUNC(Py_UNICODE *)
    PyUnicode_AsUnicodeCopy(PyObject *unicode);
PyAPI_FUNC(PyObject *) _PyUnicode_FromId(_Py_Identifier *);
PyAPI_FUNC(void) _PyUnicode_ClearStaticStrings(void);
PyAPI_FUNC(int) _PyUnicode_EQ(PyObject *, PyObject *);
#ifdef __cplusplus
}
#endif
