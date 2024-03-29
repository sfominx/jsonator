"""Test tool"""

from pathlib import Path
from subprocess import run

from jsonator.enum import ReturnCode

pytest_plugins = ["tests.addons"]

PYTHON_EXE = "python"
MODULE = "-m"
JSONATOR = "jsonator"


def test_main_file_not_found() -> None:
    """Test that main module returns FILE_NOT_FOUND if path does not exist."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, "non_existent_file.json"], check=False)
    assert process.returncode == ReturnCode.FILE_NOT_FOUND.value


def test_main_invalid_json(invalid_json: Path) -> None:
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, invalid_json], check=False)
    assert process.returncode == ReturnCode.INTERNAL_ERROR.value


def test_main_invalid_json_dir(invalid_json_in_dir: Path) -> None:
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, invalid_json_in_dir], check=False)
    assert process.returncode == ReturnCode.INTERNAL_ERROR.value


def test_main_valid_single_file_no_check(valid_format_json: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with a valid format file."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, valid_format_json], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_no_check(invalid_format_json: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with an invalid format file."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, invalid_format_json], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_single_file_check(valid_format_json: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with a valid format file and --check arg."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, "--check", valid_format_json], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_check(invalid_format_json: Path) -> None:
    """Test that main module returns SOME_FILES_WOULD_BE_REFORMATTED
    with an invalid format file and --check arg."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, "--check", invalid_format_json], check=False)
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_subdirs(valid_format_dir_no_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with a directory contains valid format files."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, valid_format_dir_no_subdirs], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_subdirs(invalid_format_dir_no_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with a directory contains invalid format files."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, invalid_format_dir_no_subdirs], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_subdirs(valid_format_dir_no_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with a directory contains valid format files and --check arg."""
    process = run(
        [PYTHON_EXE, MODULE, JSONATOR, "--check", valid_format_dir_no_subdirs], check=False
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_subdirs(invalid_format_dir_no_subdirs: Path) -> None:
    """Test that main module returns SOME_FILES_WOULD_BE_REFORMATTED
    with a directory contains invalid format files and --check arg."""
    process = run(
        [PYTHON_EXE, MODULE, JSONATOR, "--check", invalid_format_dir_no_subdirs], check=False
    )
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_recursive(valid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with valid formattted files."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, valid_format_dir_subdirs], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_recursive(invalid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with invalid format files."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, invalid_format_dir_subdirs], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_recursive(valid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with valid format files and --check arg."""
    process = run([PYTHON_EXE, MODULE, JSONATOR, "--check", valid_format_dir_subdirs], check=False)
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_recursive(invalid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with invalid format files."""
    process = run(
        [PYTHON_EXE, MODULE, JSONATOR, "--check", invalid_format_dir_subdirs], check=False
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_no_check_recursive(valid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with valid format files and --recursive arg."""
    process = run(
        [PYTHON_EXE, MODULE, JSONATOR, "--recursive", valid_format_dir_subdirs], check=False
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_recursive(invalid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE with invalid format files."""
    process = run(
        [PYTHON_EXE, MODULE, JSONATOR, "--recursive", invalid_format_dir_subdirs], check=False
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_recursive(valid_format_dir_subdirs: Path) -> None:
    """Test that main module returns NOTHING_WOULD_CHANGE
    with valid format files and --check arg."""
    process = run(
        [
            PYTHON_EXE,
            MODULE,
            JSONATOR,
            "--recursive",
            "--check",
            valid_format_dir_subdirs,
        ],
        check=False,
    )
    assert process.returncode == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_recursive(invalid_format_dir_subdirs: Path) -> None:
    """Test main module returns SOME_FILES_WOULD_BE_REFORMATTED with invalid format files."""
    process = run(
        [
            PYTHON_EXE,
            MODULE,
            JSONATOR,
            "--recursive",
            "--check",
            invalid_format_dir_subdirs,
        ],
        check=False,
    )
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_diff_colored_output(invalid_format_dir_subdirs: Path) -> None:
    """Test main module returns SOME_FILES_WOULD_BE_REFORMATTED with invalid format files."""
    process = run(
        [
            PYTHON_EXE,
            MODULE,
            JSONATOR,
            "--recursive",
            "--check",
            "--diff",
            "--color",
            invalid_format_dir_subdirs,
        ],
        check=False,
    )
    assert process.returncode == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value
