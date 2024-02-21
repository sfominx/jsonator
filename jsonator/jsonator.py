"""
Format JSON using json tool
"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING, Any

from jsonator import output

if TYPE_CHECKING:
    from pathlib import Path

    from jsonator.models import ModeArgs
    from jsonator.report import Report

UTF_8 = "utf-8"


def format_json_file(  # pylint: disable=too-many-arguments,too-many-branches,too-many-locals
    json_file: Path, report: Report, mode_args: ModeArgs, dump_args: dict[str, Any]
) -> None:
    """
    This function formats the file in JSON format.
    It uses the json.tool module, built into Python, to create a readable JSON format.
    """
    logging.basicConfig(format="%(message)s")

    try:
        input_json_data = json_file.read_text(encoding=UTF_8)

    except FileNotFoundError:
        report.failed(json_file, "File not found")
        return

    try:
        input_json = json.loads(input_json_data)

    except json.decoder.JSONDecodeError as exc:
        report.failed(json_file, exc.msg)
        return

    output_json_data = json.dumps(input_json, **dump_args) + "\n"
    is_identical = input_json_data == output_json_data

    if not is_identical and not mode_args.check:
        json_file.write_text(output_json_data, encoding=UTF_8)

    report.done(json_file, not is_identical)

    if mode_args.diff:
        diff_contents = output.diff(
            input_json_data,
            output_json_data,
            json_file.name,
            "formatted file",
        )

        if mode_args.color:
            diff_contents = output.color_diff(diff_contents)

        logging.info(diff_contents)
