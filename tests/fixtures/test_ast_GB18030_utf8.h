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
