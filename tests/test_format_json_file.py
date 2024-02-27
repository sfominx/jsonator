"""
Tests for the format_json_file function
"""

import json
from pathlib import Path

import pytest

from jsonator.enum import ReturnCode
from jsonator.jsonator import format_json_file
from jsonator.models import ModeArgs
from jsonator.report import Report

# pylint: disable=redefined-outer-name

FILES_ENCODING = "utf-8"


@pytest.fixture()
def json_file(tmp_path: Path) -> Path:
    """Create a temporary file for testing"""
    file_path = tmp_path / "test.json"
    data = {"key": "value"}
    file_path.write_text(json.dumps(data), encoding=FILES_ENCODING)
    return file_path


@pytest.fixture()
def json_file_incorrect_format(tmp_path: Path) -> Path:
    """Create a temporary file for testing"""
    file_path = tmp_path / "test_incorrect.json"
    file_path.write_text('{"key": "value"}')
    return file_path


def test_format_json_file(json_file: Path, json_file_incorrect_format: Path) -> None:
    """Test format_json_file function"""
    # Test formatting with corectly formatted file
    report = Report(check=False, diff=False)
    dump_args = {
        "sort_keys": False,
        "indent": 4,
        "ensure_ascii": False,
    }
    format_json_file(json_file, report, ModeArgs(False, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.NOTHING_WOULD_CHANGE.value

    # Test checking format with corectly formatted file
    report = Report(check=True, diff=False)
    format_json_file(json_file, report, ModeArgs(True, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.NOTHING_WOULD_CHANGE.value

    # Test checking format with corectly formatted file, but 2 spaces indentation
    dump_args["indent"] = 2
    report = Report(check=True, diff=False)
    format_json_file(json_file, report, ModeArgs(True, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

    # Test checking format with corectly formatted file, but tab indentation
    dump_args["indent"] = "\t"  # type: ignore[assignment]
    report = Report(check=True, diff=False)
    format_json_file(json_file, report, ModeArgs(True, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

    # Test checking format with corectly formatted file, but no indentation
    report = Report(check=True, diff=False)
    format_json_file(json_file, report, ModeArgs(True, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

    # Test checking format with corectly formatted file, but compact formatting
    report = Report(check=True, diff=False)
    format_json_file(json_file, report, ModeArgs(True, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

    # Test checking format with incorectly formatted file
    report = Report(check=True, diff=False)
    format_json_file(
        json_file_incorrect_format, report, ModeArgs(True, False, False), dump_args=dump_args
    )
    assert report.status == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

    # Test checking format with incorectly formatted file
    report = Report(check=False, diff=False)
    format_json_file(
        json_file_incorrect_format,
        report,
        ModeArgs(False, False, False),
        dump_args=dump_args,
    )
    assert report.status == ReturnCode.NOTHING_WOULD_CHANGE.value

    # Test with non-existing file
    report = Report(check=False, diff=False)
    format_json_file(
        Path("non_existing_file.json"),
        report,
        ModeArgs(False, False, False),
        dump_args=dump_args,
    )
    assert report.status == ReturnCode.INTERNAL_ERROR.value

    # Test with a non-json file
    report = Report(check=False, diff=False)
    non_json_file = Path(json_file.parent, "test.txt")
    non_json_file.write_text("hello world", encoding=FILES_ENCODING)
    format_json_file(non_json_file, report, ModeArgs(False, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.INTERNAL_ERROR.value

    # Test with a malformed json file
    report = Report(check=False, diff=False)
    malformed_file = Path(json_file.parent, "malformed.json")
    malformed_file.write_text("{", encoding=FILES_ENCODING)
    format_json_file(malformed_file, report, ModeArgs(False, False, False), dump_args=dump_args)
    assert report.status == ReturnCode.INTERNAL_ERROR.value
