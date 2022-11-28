import re
import logging
import pathlib
from collections import namedtuple
import subprocess

import charset_normalizer
import clang_format

import common.init_log

logger = logging.getLogger(__name__)


# todo: The result of charset_normalizer dectected encoding in chinese is not accurate.
def convert_encoding(input: str, output: str, encoding: str = "utf-8"):
    """convert text file to specify encoding (default: utf-8).
    Detect encoding of input file by charset-normalizer lib.


    Args:
        input (str): input file path.
        output (str): output file path.
        encoding (str): encoding of output file.
    """
    input_path = pathlib.Path(input)
    output_path = pathlib.Path(output)

    try:
        guess_best = charset_normalizer.from_path(input_path).best()
        if not guess_best:
            logger.warning(f'Failed to detect encoding of {input}')
            logger.warning(f'Give up convert encoding to utf-8')
        guess_encoding = guess_best.encoding
        if guess_encoding != encoding:
            logger.debug(f"Detected {input_path} using encoding: {guess_encoding}")
            output_path.write_text(
                input_path.read_text(encoding=guess_encoding), encoding=encoding
            )
            logger.debug(
                f"Converted from {input_path}:{guess_encoding} to {output}:{encoding}"
            )
    except (FileNotFoundError, UnicodeDecodeError, UnicodeEncodeError) as e:
        logger.error(e)


def clean_multiple_spaces(input_text: str):
    ReSub = namedtuple("ReSub", ["pattern", "repl"])
    resubs = {
        "dos2unix": ReSub(r"\r\n", "\n"),
        "clean_multi_lf": ReSub(r"\n+", "\n"),
        "clean_multi_space": ReSub(r"[ \t\r\x0b\x0c]+", " "),
        "clean_tail_line_space": ReSub(r"\s+\n", "\n"),
    }
    for resub in resubs.values():
        input_text = re.sub(resub.pattern, resub.repl, input_text)
        logger.debug(f"Cleaned spaces in text by {resub}")

    return input_text


def clean_clike_comments(input_text: str):
    def replacer(match):
        s = match.group(0)
        if s.startswith("/"):
            return ""
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    clean_comments_text = re.sub(pattern, replacer, input_text)
    logger.debug(f"Cleaned comments in text.")
    return clean_comments_text


def run_clang_format(input: str):
    """Run clang-format with specify file. Depends on clang_format lib.

    Args:
        input (str): input file path.
    """
    clang_format_bin = clang_format._get_executable("clang-format")
    clang_format_args = ["--sort-includes", "-i", input]
    clang_format_cmd = [clang_format_bin] + clang_format_args

    try:
        subprocess.run(clang_format_cmd, check=True)
        logger.debug(f"clang-format: {clang_format_cmd}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to clang-format with {input}", e)

# todo: preprocess https://github.com/ned14/pcpp
def normalize_clike(input: str, output: str):
    output_path = pathlib.Path(output)
    
    try:
        convert_encoding(input, output)
        output_text = output_path.read_text('utf-8')
        output_text = clean_clike_comments(output_text)
        output_text = clean_multiple_spaces(output_text)
        output_path.write_text(output_text, encoding='utf-8')
        run_clang_format(output)
        if input == output:
            logger.info(f'Nomalized {input} IN PLACE.')
        else:
            logger.info(f'Nomalized from {input} to {output}')
        
    except (FileNotFoundError, UnicodeDecodeError, UnicodeEncodeError) as e:
        logger.error(e)


if __name__ == "__main__":
    fn_in = "./tests/fixtures/ast_GB18030.h"
    fn_out = "./tests/fixtures/test_ast_GB18030_utf8.h"
    normalize_clike(fn_out, fn_out)
