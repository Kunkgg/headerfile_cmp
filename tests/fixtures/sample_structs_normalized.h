
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
