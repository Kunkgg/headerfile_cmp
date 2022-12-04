import pathlib

from headerfile_ast import dump_ast
from headerfile_formatter import normalize_clike
from headerfile_parser import HeaderFileParser

FIXTURES_PATH = pathlib.Path("./tests/fixtures")


def prepare_parser_sample(fn: str):
    fn_path = FIXTURES_PATH / fn
    fn_normailezed_path = FIXTURES_PATH / f"{fn_path.stem}_normalized.h"
    json_path = FIXTURES_PATH / f"{fn_path.stem}_normalized.json"
    normalize_clike(str(fn_path), str(fn_normailezed_path))
    dump_ast(str(fn_normailezed_path), str(json_path))
    return HeaderFileParser(str(fn_normailezed_path))