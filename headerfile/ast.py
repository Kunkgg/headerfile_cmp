import logging

import CppHeaderParser


logger = logging.getLogger(__name__)


def dump_ast(input: str, output: str):
    ast = CppHeaderParser.CppHeader(input)
    with open(output, "w") as fp:
        fp.write(ast.toJSON())
    logger.info(f"Dumped AST: from {input} to {output}")


if __name__ == "__main__":
    input = "./tests/fixtures/sample_normalized.h"
    output = "./tests/fixtures/sample_normalized.json"
    dump_ast(input, output)
