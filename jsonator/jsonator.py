"""
Format JSON using json tool
"""
import filecmp
import os
import random
import shutil
import string
import sys
from pathlib import Path
from subprocess import PIPE, STDOUT, run
from tempfile import gettempdir
from typing import List, Optional, Union

from jsonator import output
from jsonator.report import Report

FILES_ENCODING = "utf-8"


def random_str() -> str:
    """Generating a random alphanumeric string of 8 characters long"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=8))


def make_temp_file() -> Path:
    """Generate temp file path"""
    temp_dir = Path(gettempdir()).absolute()
    temp_file = temp_dir / random_str()

    while temp_file.exists():
        temp_file = temp_dir / random_str()

    return temp_file


def format_json_file(  # pylint: disable=too-many-arguments,too-many-branches,too-many-locals
    json_file: Path,
    report: Report,
    check: bool,
    diff: bool,
    color: bool,
    sort_keys: bool,
    indent: Optional[int],
    tab: bool,
    no_indent: bool,
    compact: bool,
    no_ensure_ascii: bool,
) -> None:
    """
    This function formats the file in JSON format.
    It uses the json.tool module, built into Python, to create a readable JSON format.
    """
    tmp_file = make_temp_file()

    cmd: List[Union[str, Path]] = [sys.executable, "-m", "json.tool", json_file, tmp_file]
    if sort_keys:
        cmd.append("--sort-keys")
    if indent is not None:
        cmd.extend(["--indent", str(indent)])
    if tab:
        cmd.append("--tab")
    if no_indent:
        cmd.append("--no-indent")
    if compact:
        cmd.append("--compact")
    if no_ensure_ascii:
        cmd.append("--no-ensure-ascii")

    execution_result = run(cmd, stdout=PIPE, stderr=STDOUT, check=False)

    if execution_result.returncode or execution_result.stdout:
        report.failed(json_file, execution_result.stdout.decode(FILES_ENCODING))
        return

    try:
        is_identical = filecmp.cmp(json_file, tmp_file, shallow=False)
    except FileNotFoundError:
        report.failed(json_file, "Internal error")
        return

    report.done(json_file, not is_identical)

    if diff:
        diff_contents = output.diff(
            json_file.read_text(encoding=FILES_ENCODING),
            tmp_file.read_text(encoding=FILES_ENCODING),
            json_file.name,
            "formatted file",
        )

        if color:
            diff_contents = output.color_diff(diff_contents)

        print(diff_contents)

    if tmp_file.exists():
        if check or diff:
            os.unlink(tmp_file)
        else:
            os.unlink(json_file)
            shutil.copy(tmp_file, json_file)
            os.unlink(tmp_file)
    else:
        report.failed(json_file, "Internal error")
