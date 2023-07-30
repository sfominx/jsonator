"""
Tests for the format_json_file function
"""
import json
import sys
from pathlib import Path

import pytest

# pylint: disable=import-error,wrong-import-position,redefined-outer-name

sys.path.append(str(Path(__file__).resolve().parent.parent))

from jsonator.jsonator import ReturnCode, format_json_file

FILES_ENCODING = "utf-8"


@pytest.fixture
def json_file(tmp_path: Path) -> Path:
    """Create a temporary file for testing"""
    file_path = tmp_path / "test.json"
    data = {"key": "value"}
    with open(file_path, "w", encoding=FILES_ENCODING) as file_descriptor:
        json.dump(data, file_descriptor)
    return file_path


@pytest.fixture
def json_file_incorrect_format(tmp_path: Path) -> Path:
    """Create a temporary file for testing"""
    file_path = tmp_path / "test_incorrect.json"
    file_path.write_text('{"key": "value"}')
    return file_path


def test_format_json_file(json_file: Path, json_file_incorrect_format: Path) -> None:
    """Test format_json_file function"""
    # Test formatting with corectly formatted file
    assert (
        format_json_file(json_file, check=False, diff=False, color=False, sort_keys=False)
        == ReturnCode.NOTHING_WOULD_CHANGE
    )

    # Test checking format with corectly formatted file
    assert (
        format_json_file(json_file, check=True, diff=False, color=False, sort_keys=False)
        == ReturnCode.NOTHING_WOULD_CHANGE
    )

    # Test checking format with incorectly formatted file
    assert (
        format_json_file(
            json_file_incorrect_format, check=True, diff=False, color=False, sort_keys=False
        )
        == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED
    )

    # Test checking format with incorectly formatted file
    assert (
        format_json_file(
            json_file_incorrect_format, check=False, diff=False, color=False, sort_keys=False
        )
        == ReturnCode.NOTHING_WOULD_CHANGE
    )

    # Test with non-existing file
    assert (
        format_json_file(
            Path("non_existing_file.json"), check=False, diff=False, color=False, sort_keys=False
        )
        == ReturnCode.INTERNAL_ERROR
    )

    # Test with a non-json file
    non_json_file = Path(json_file.parent, "test.txt")
    non_json_file.write_text("hello world", encoding=FILES_ENCODING)
    assert (
        format_json_file(non_json_file, check=False, diff=False, color=False, sort_keys=False)
        == ReturnCode.INTERNAL_ERROR
    )

    # Test with a malformed json file
    malformed_file = Path(json_file.parent, "malformed.json")
    malformed_file.write_text("{", encoding=FILES_ENCODING)
    assert (
        format_json_file(malformed_file, check=False, diff=False, color=False, sort_keys=False)
        == ReturnCode.INTERNAL_ERROR
    )
