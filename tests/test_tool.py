import sys
from pathlib import Path
from subprocess import run

from jsonator.jsonator import ReturnCode
from tests.addons import INTERPRETER

# pylint: disable=import-error,wrong-import-position,redefined-outer-name

PROJECT_ROOT = Path(__file__).resolve().parent.parent
# sys.path.append(str(PROJECT_ROOT))


pytest_plugins = ["addons"]


def test_main_file_not_found():
    """Test that main module returns FILE_NOT_FOUND if path does not exist."""
    process = run(["jsonator", "non_existent_file.json"])
    assert process.returncode == ReturnCode.FILE_NOT_FOUND.value


def test_main_invalid_json(invalid_json: Path):
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    process = run(["jsonator", invalid_json])
    assert process.returncode == ReturnCode.INTERNAL_ERROR.value


def test_main_invalid_json_dir(invalid_json_in_dir: Path):
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    process = run(["jsonator", invalid_json_in_dir])
    assert process.returncode == ReturnCode.INTERNAL_ERROR.value


def test_main_valid_single_file_no_check(valid_format_json: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with a valid format file."""
    process = run(["jsonator", valid_format_json])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_no_check(invalid_format_json: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with an invalid format file."""
    process = run(["jsonator", invalid_format_json])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_single_file_check(valid_format_json: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with a valid format file and --check arg."""
    process = run(["jsonator", "--check", valid_format_json])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_check(invalid_format_json: Path):
    """Test that main module returns SOME_FILES_WOULD_BE_REFORMATTED with an invalid format file and --check arg."""
    process = run(["jsonator", "--check", invalid_format_json])
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_subdirs(valid_format_dir_no_subdirs: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with a directory contains valid format files."""
    process = run(["jsonator", valid_format_dir_no_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_subdirs(invalid_format_dir_no_subdirs: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with a directory contains invalid format files."""
    process = run(["jsonator", invalid_format_dir_no_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_subdirs(valid_format_dir_no_subdirs: Path):
    """Test that main module returns NOTHING_WOULD_CHANGE with a directory contains valid format files and --check arg."""
    process = run(["jsonator", "--check", valid_format_dir_no_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_subdirs(invalid_format_dir_no_subdirs: Path):
    """Test that main module returns SOME_FILES_WOULD_BE_REFORMATTED with a directory contains invalid format files and --check arg."""
    process = run(["jsonator", "--check", invalid_format_dir_no_subdirs])
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_recursive(valid_format_dir_subdirs: Path):
    process = run(["jsonator", valid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_recursive(invalid_format_dir_subdirs: Path):
    process = run(["jsonator", invalid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_recursive(valid_format_dir_subdirs: Path):
    process = run(["jsonator", "--check", valid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_recursive(invalid_format_dir_subdirs: Path):
    process = run(["jsonator", "--check", invalid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_no_check_recursive(valid_format_dir_subdirs: Path):
    process = run(["jsonator", "--recursive", valid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_recursive(invalid_format_dir_subdirs: Path):
    process = run(["jsonator", "--recursive", invalid_format_dir_subdirs])
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_recursive(valid_format_dir_subdirs: Path):
    process = run(
        [
            "jsonator",
            "--recursive",
            "--check",
            valid_format_dir_subdirs,
        ]
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_recursive(invalid_format_dir_subdirs: Path):
    process = run(
        [
            "jsonator",
            "--recursive",
            "--check",
            invalid_format_dir_subdirs,
        ]
    )
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value
