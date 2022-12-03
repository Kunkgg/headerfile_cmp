import re
import logging
import pathlib
from collections import namedtuple
import subprocess

import charset_normalizer
import clang_format

import common.init_log

logger = logging.getLogger(__name__)

ReSub = namedtuple("ReSub", ["pattern", "repl"])

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
            logger.warning(f"Failed to detect encoding of {input}")
            logger.warning(f"Give up convert encoding to utf-8")
            return
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


def combine_splited_line(input_text: str):
    resub = ReSub(r"[\s\\]+", " ")  # 将反斜杠分割的的多行合并为一行
    input_text = re.sub(resub.pattern, resub.repl, input_text)
    logger.debug(f"Combined splited line by {resub}")
    return input_text


def clean_line_tailed(input_text: str):
    RESUB_MAP = {
        "dos2unix": ReSub(r"\r\n", "\n"),
        "multi_lf": ReSub(r"\n+", "\n"),
        "tailed_space": ReSub(r"\s+\n", "\n"),
    }
    for resub in RESUB_MAP.values():
        input_text = re.sub(resub.pattern, resub.repl, input_text)
        logger.debug(f"Cleaned tailed in text by {resub}")

    return input_text


def clean_multiple_whitespaces(input_text: str, lf: bool = False):
    RESUB_MAP = {
        "multi_space": ReSub(r"[ \t\r\x0b\x0c]+", " "),
        "multi_space_include_lf": ReSub(r"\s+", " "),
    }
    resub = RESUB_MAP["multi_space_include_lf"] if lf else RESUB_MAP["multi_space"]
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
        output_text = output_path.read_text("utf-8")
        output_text = clean_clike_comments(output_text)
        output_text = clean_line_tailed(output_text)
        output_text = clean_multiple_whitespaces(output_text)
        output_path.write_text(output_text, encoding="utf-8")
        run_clang_format(output)
        if input == output:
            logger.info(f"Nomalized {input} IN PLACE.")
        else:
            logger.info(f"Nomalized from {input} to {output}")

    except (FileNotFoundError, UnicodeDecodeError, UnicodeEncodeError) as e:
        logger.error(e)


if __name__ == "__main__":
    fn_sample = "./tests/fixtures/sample.h"
    fn_sample_normalized = "./tests/fixtures/sample_normalized.h"
    normalize_clike(fn_sample, fn_sample_normalized)
