import pathlib

from headerfile.ast import dump_ast
from headerfile.formatter import normalize_clike
from headerfile.parser import HeaderFileParser
from headerfile.comparator import HeaderFileComparator

FIXTURES_PATH = pathlib.Path("./tests/fixtures")


def prepare_parser_sample(fn: str):
    fn_path = FIXTURES_PATH / fn
    fn_normailezed_path = fn_path.parent / f"{fn_path.stem}_normalized.h"
    json_path = fn_path.parent / f"{fn_path.stem}_normalized.json"
    normalize_clike(str(fn_path), str(fn_normailezed_path))
    dump_ast(str(fn_normailezed_path), str(json_path))
    return HeaderFileParser(str(fn_normailezed_path))


def prepare_comparator_sample(subdir):
    fn = f"{subdir}/sample.h"
    fn_cp = f"{subdir}/sample_copy.h"
    fn_modi = f"{subdir}/sample_modified.h"
    fn_modi_seq = f"{subdir}/sample_modified_sequence.h"
    fn_modi_add = f"{subdir}/sample_modified_add.h"
    fn_modi_del = f"{subdir}/sample_modified_del.h"

    parsed = prepare_parser_sample(fn).parse()
    parsed_cp = prepare_parser_sample(fn_cp).parse()
    parsed_modi = prepare_parser_sample(fn_modi).parse()
    parsed_modi_seq = prepare_parser_sample(fn_modi_seq).parse()
    parsed_modi_add = prepare_parser_sample(fn_modi_add).parse()
    parsed_modi_del = prepare_parser_sample(fn_modi_del).parse()

    cmptor_cp = HeaderFileComparator(parsed, parsed_cp)
    cmptor_modi = HeaderFileComparator(parsed, parsed_modi)
    cmptor_modi_seq = HeaderFileComparator(parsed, parsed_modi_seq)
    cmptor_modi_add = HeaderFileComparator(parsed, parsed_modi_add)
    cmptor_modi_del = HeaderFileComparator(parsed, parsed_modi_del)

    return cmptor_cp, cmptor_modi, cmptor_modi_seq, cmptor_modi_add, cmptor_modi_del


def prepare_comparator_sample_seq_inner(subdir):
    fn = f"{subdir}/sample.h"
    fn_modi_seq_inner = f"{subdir}/sample_modified_sequence_inner.h"
    parsed = prepare_parser_sample(fn).parse()
    parsed_modi_seq_inner = prepare_parser_sample(fn_modi_seq_inner).parse()
    cmptor_modi_seq_inner = HeaderFileComparator(parsed, parsed_modi_seq_inner)

    return cmptor_modi_seq_inner
