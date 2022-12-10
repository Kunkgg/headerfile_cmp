enum PyUnicode_Kind {
/* String contains only wstr byte characters.  This is only possible
   when the string was created with a legacy API and _PyUnicode_Ready()
   has not been called yet.  */
    PyUnicode_WCHAR_KIND = 0,
/* Return values of the PyUnicode_KIND() macro: */
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