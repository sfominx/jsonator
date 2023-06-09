import argparse
import sys
from pathlib import Path

from jsonator import main
from jsonator.jsonator import ReturnCode

# pylint: disable=import-error,wrong-import-position,redefined-outer-name

# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# sys.path.append(str(PROJECT_ROOT))

FILES_ENCODING = "utf-8"
INTERPRETER = Path(sys.executable).stem

pytest_plugins = ["addons"]


def test_main_file_not_found(mocker):
    """Test that main module returns FILE_NOT_FOUND if path does not exist."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=Path("/path/to/file.json"), recursive=False, check=False
        ),
    )
    assert main() == ReturnCode.FILE_NOT_FOUND.value


def test_main_invalid_json(mocker, invalid_json: Path):
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=invalid_json, recursive=False, check=False),
    )
    assert main() == ReturnCode.INTERNAL_ERROR.value


def test_main_invalid_json_dir(mocker, invalid_json_in_dir: Path):
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=invalid_json_in_dir, recursive=False, check=False),
    )
    assert main() == ReturnCode.INTERNAL_ERROR.value


def test_main_valid_single_file_no_check(mocker, valid_format_json: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with a valid format file."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=valid_format_json, recursive=False, check=False),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_no_check(mocker, invalid_format_json: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with an invalid format file."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=invalid_format_json, recursive=False, check=False),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_single_file_check(mocker, valid_format_json: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with a valid format file and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=valid_format_json, recursive=False, check=True),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_check(mocker, invalid_format_json: Path):
    """Test that main function returns SOME_FILES_WOULD_BE_REFORMATTED with an invalid format file and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=invalid_format_json, recursive=False, check=True),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_subdirs(mocker, valid_format_dir_no_subdirs: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains valid format files."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_no_subdirs, recursive=False, check=False
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_subdirs(mocker, invalid_format_dir_no_subdirs: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains invalid format files."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_no_subdirs, recursive=False, check=False
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_subdirs(mocker, valid_format_dir_no_subdirs: Path):
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains valid format files and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_no_subdirs, recursive=False, check=True
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_subdirs(mocker, invalid_format_dir_no_subdirs: Path):
    """Test that main function returns SOME_FILES_WOULD_BE_REFORMATTED with a directory contains invalid format files and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_no_subdirs, recursive=False, check=True
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_recursive(mocker, valid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_subdirs, recursive=False, check=False
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_recursive(mocker, invalid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs, recursive=False, check=False
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_recursive(mocker, valid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=valid_format_dir_subdirs, recursive=False, check=True),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_recursive(mocker, invalid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs, recursive=False, check=True
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_no_check_recursive(mocker, valid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=valid_format_dir_subdirs, recursive=True, check=False),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_recursive(mocker, invalid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs, recursive=True, check=False
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_recursive(mocker, valid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(path=valid_format_dir_subdirs, recursive=True, check=True),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_recursive(mocker, invalid_format_dir_subdirs: Path):
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs, recursive=True, check=True
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value
