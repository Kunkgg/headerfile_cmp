/* --- _PyUnicodeWriter API ----------------------------------------------- */

typedef struct
{
    PyObject *buffer;
    void *data;
    enum PyUnicode_Kind kind;
    Py_UCS4 maxchar;
    Py_ssize_t size;
    Py_ssize_t pos;

    /* minimum number of allocated characters (default: 0) */
    Py_ssize_t min_length;

    /* minimum character (default: 127, ASCII) */
    Py_UCS4 min_char;

    /* If non-zero, overallocate the buffer (default: 0). */
    unsigned char overallocate;

    /* If readonly is 1, buffer is a shared string (cannot be modified)
       and size is set to 0. */
    unsigned char readonly;
} _PyUnicodeWriter;

/* ASCII-only strings created through PyUnicode_New use the PyASCIIObject
   structure. state.ascii and state.compact are set, and the data
   immediately follow the structure. utf8_length and wstr_length can be found
   in the length field; the utf8 pointer is equal to the data pointer. */
typedef struct
{
    /* There are 4 forms of Unicode strings:

       - compact ascii:

         * structure = PyASCIIObject
         * test: PyUnicode_IS_COMPACT_ASCII(op)
         * kind = PyUnicode_1BYTE_KIND
         * compact = 1
         * ascii = 1
         * ready = 1
         * (length is the length of the utf8 and wstr strings)
         * (data starts just after the structure)
         * (since ASCII is decoded from UTF-8, the utf8 string are the data)

       - compact:

         * structure = PyCompactUnicodeObject
         * test: PyUnicode_IS_COMPACT(op) && !PyUnicode_IS_ASCII(op)
         * kind = PyUnicode_1BYTE_KIND, PyUnicode_2BYTE_KIND or
           PyUnicode_4BYTE_KIND
         * compact = 1
         * ready = 1
         * ascii = 0
         * utf8 is not shared with data
         * utf8_length = 0 if utf8 is NULL
         * wstr is shared with data and wstr_length=length
           if kind=PyUnicode_2BYTE_KIND and sizeof(wchar_t)=2
           or if kind=PyUnicode_4BYTE_KIND and sizeof(wchar_t)=4
         * wstr_length = 0 if wstr is NULL
         * (data starts just after the structure)

       - legacy string, not ready:

         * structure = PyUnicodeObject
         * test: kind == PyUnicode_WCHAR_KIND
         * length = 0 (use wstr_length)
         * hash = -1
         * kind = PyUnicode_WCHAR_KIND
         * compact = 0
         * ascii = 0
         * ready = 0
         * interned = SSTATE_NOT_INTERNED
         * wstr is not NULL
         * data.any is NULL
         * utf8 is NULL
         * utf8_length = 0

       - legacy string, ready:

         * structure = PyUnicodeObject structure
         * test: !PyUnicode_IS_COMPACT(op) && kind != PyUnicode_WCHAR_KIND
         * kind = PyUnicode_1BYTE_KIND, PyUnicode_2BYTE_KIND or
           PyUnicode_4BYTE_KIND
         * compact = 0
         * ready = 1
         * data.any is not NULL
         * utf8 is shared and utf8_length = length with data.any if ascii = 1
         * utf8_length = 0 if utf8 is NULL
         * wstr is shared with data.any and wstr_length = length
           if kind=PyUnicode_2BYTE_KIND and sizeof(wchar_t)=2
           or if kind=PyUnicode_4BYTE_KIND and sizeof(wchar_4)=4
         * wstr_length = 0 if wstr is NULL

       Compact strings use only one memory block (structure + characters),
       whereas legacy strings use one block for the structure and one block
       for characters.

       Legacy strings are created by PyUnicode_FromUnicode() and
       PyUnicode_FromStringAndSize(NULL, size) functions. They become ready
       when PyUnicode_READY() is called.

       See also _PyUnicode_CheckConsistency().
    */
    PyObject_HEAD
        Py_ssize_t length; /* Number of code points in the string */
    Py_hash_t hash;        /* Hash value; -1 if not set */
    struct
    {
        /*
           SSTATE_NOT_INTERNED (0)
           SSTATE_INTERNED_MORTAL (1)
           SSTATE_INTERNED_IMMORTAL (2)

           If interned != SSTATE_NOT_INTERNED, the two references from the
           dictionary to this object are *not* counted in ob_refcnt.
         */
        unsigned int interned : 2;
        /* Character size:

           - PyUnicode_WCHAR_KIND (0):

             * character type = wchar_t (16 or 32 bits, depending on the
               platform)

           - PyUnicode_1BYTE_KIND (1):

             * character type = Py_UCS1 (8 bits, unsigned)
             * all characters are in the range U+0000-U+00FF (latin1)
             * if ascii is set, all characters are in the range U+0000-U+007F
               (ASCII), otherwise at least one character is in the range
               U+0080-U+00FF

           - PyUnicode_2BYTE_KIND (2):

             * character type = Py_UCS2 (16 bits, unsigned)
             * all characters are in the range U+0000-U+FFFF (BMP)
             * at least one character is in the range U+0100-U+FFFF

           - PyUnicode_4BYTE_KIND (4):

             * character type = Py_UCS4 (32 bits, unsigned)
             * all characters are in the range U+0000-U+10FFFF
             * at least one character is in the range U+10000-U+10FFFF
         */
        unsigned int kind : 3;
        /* Compact is with respect to the allocation scheme. Compact unicode
           objects only require one memory block while non-compact objects use
           one block for the PyUnicodeObject struct and another for its data
           buffer. */
        unsigned int compact : 1;
        /* The string only contains characters in the range U+0000-U+007F (ASCII)
           and the kind is PyUnicode_1BYTE_KIND. If ascii is set and compact is
           set, use the PyASCIIObject structure. */
        unsigned int ascii : 1;
        /* The ready flag indicates whether the object layout is initialized
           completely. This means that this is either a compact object, or
           the data pointer is filled out. The bit is redundant, and helps
           to minimize the test in PyUnicode_IS_READY(). */
        unsigned int ready : 1;
        /* Padding to ensure that PyUnicode_DATA() is always aligned to
           4 bytes (see issue #19537 on m68k). */
        unsigned int : 24;
    } state;
    wchar_t *wstr; /* wchar_t representation (null-terminated) */
} PyASCIIObject;

/* Non-ASCII strings allocated through PyUnicode_New use the
   PyCompactUnicodeObject structure. state.compact is set, and the data
   immediately follow the structure. */
typedef struct
{
    PyASCIIObject _base;
    Py_ssize_t utf8_length; /* Number of bytes in utf8, excluding the
                             * terminating \0. */
    char *utf8;             /* UTF-8 representation (null-terminated) */
    Py_ssize_t wstr_length; /* Number of code points in wstr, possible
                             * surrogates count as two code points. */
} PyCompactUnicodeObject;

/* Strings allocated through PyUnicode_FromUnicode(NULL, len) use the
   PyUnicodeObject structure. The actual string data is initially in the wstr
   block, and copied into the data block using _PyUnicode_Ready. */
typedef struct
{
    PyCompactUnicodeObject _base;
    union
    {
        void *any;
        Py_UCS1 *latin1;
        Py_UCS2 *ucs2;
        Py_UCS4 *ucs4;
    } data; /* Canonical, smallest-form Unicode buffer */
} PyUnicodeObject;
