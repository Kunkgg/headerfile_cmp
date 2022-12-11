import logging

from common import init_log
from headerfile.parser import HeaderFileParser


init_log.setup()

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    fn = "./tests/fixtures/sample_normalized.h"
    fn_json = "./tests/fixtures/parsed_sample_normalized.json"
    parser = HeaderFileParser(fn)
    print(parser.parse())
    parsed_dict = parser.to_dict()
    parser.to_json(fn_json)

    from tests.prepare import prepare_comparator_sample

    subdir = "sample_is_same"

    (
        cmptor_cp,
        cmptor_modi,
        cmptor_modi_seq,
        cmptor_modi_add,
        cmptor_modi_del,
    ) = prepare_comparator_sample(subdir)

    print(cmptor_modi.compare())
    cmp_dict = cmptor_modi.to_dict()
    fn_json = "./tests/fixtures/compared_sample.json"
    cmptor_modi.to_json(fn_json)
