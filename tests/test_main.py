"""Test main module."""
import argparse
import sys
from pathlib import Path

from pytest_mock import MockerFixture

from jsonator import main  # pylint: disable=import-error
from jsonator.enum import ReturnCode  # pylint: disable=import-error

FILES_ENCODING = "utf-8"
INTERPRETER = Path(sys.executable).stem

pytest_plugins = ["addons"]


def test_main_file_not_found(mocker: MockerFixture) -> None:
    """Test that main module returns FILE_NOT_FOUND if path does not exist."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=Path("/path/to/file.json"),
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.FILE_NOT_FOUND.value


def test_main_invalid_json(mocker: MockerFixture, invalid_json: Path) -> None:
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_json,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.INTERNAL_ERROR.value


def test_main_invalid_json_dir(mocker: MockerFixture, invalid_json_in_dir: Path) -> None:
    """Test that main module returns INTERNAL_ERROR if json file has invalid syntax."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_json_in_dir,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.INTERNAL_ERROR.value


def test_main_valid_single_file_no_check(mocker: MockerFixture, valid_format_json: Path) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE with a valid format file."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_json,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_single_file_no_check(
    mocker: MockerFixture, invalid_format_json: Path
) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE with an invalid format file."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_json,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_single_file_check(mocker: MockerFixture, valid_format_json: Path) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE
    with a valid format file and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_json,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_single_file_check_sort_keys(
    mocker: MockerFixture, invalid_format_json_multiple_keys: Path
) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE
    with a valid format file and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_json_multiple_keys,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=True,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_invalid_single_file_check(mocker: MockerFixture, invalid_format_json: Path) -> None:
    """Test that main function returns SOME_FILES_WOULD_BE_REFORMATTED with
    an invalid format file and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_json,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_subdirs(
    mocker: MockerFixture, valid_format_dir_no_subdirs: Path
) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains
    valid format files."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_no_subdirs,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_subdirs(
    mocker: MockerFixture, invalid_format_dir_no_subdirs: Path
) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains
    invalid format files."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_no_subdirs,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_subdirs(
    mocker: MockerFixture, valid_format_dir_no_subdirs: Path
) -> None:
    """Test that main function returns NOTHING_WOULD_CHANGE with a directory contains valid format
    files and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_no_subdirs,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_subdirs(
    mocker: MockerFixture, invalid_format_dir_no_subdirs: Path
) -> None:
    """Test that main function returns SOME_FILES_WOULD_BE_REFORMATTED with a directory contains
    invalid format files and --check arg."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_no_subdirs,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value


def test_main_valid_dir_no_check_no_recursive(
    mocker: MockerFixture, valid_format_dir_subdirs: Path
) -> None:
    """Test main function with a valid directory path, without check and without recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_subdirs,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_no_recursive(
    mocker: MockerFixture, invalid_format_dir_subdirs: Path
) -> None:
    """Test main function with an invalid directory path, without check and without recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs,
            recursive=False,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_no_recursive(
    mocker: MockerFixture, valid_format_dir_subdirs: Path
) -> None:
    """Test main function with a valid directory path, with check and without recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_subdirs,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_no_recursive(
    mocker: MockerFixture, invalid_format_dir_subdirs: Path
) -> None:
    """Test main function with an invalid directory path, with check and without recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs,
            recursive=False,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_no_check_recursive(
    mocker: MockerFixture, valid_format_dir_subdirs: Path
) -> None:
    """Test main function with a valid directory path, without check and with recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_subdirs,
            recursive=True,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_no_check_recursive(
    mocker: MockerFixture, invalid_format_dir_subdirs: Path
) -> None:
    """Test main function with an invalid directory path, without check and with recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs,
            recursive=True,
            check=False,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_valid_dir_check_recursive(
    mocker: MockerFixture, valid_format_dir_subdirs: Path
) -> None:
    """Test main function with a valid directory path, with check and with recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=valid_format_dir_subdirs,
            recursive=True,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.NOTHING_WOULD_CHANGE.value


def test_main_invalid_dir_check_recursive(
    mocker: MockerFixture, invalid_format_dir_subdirs: Path
) -> None:
    """Test main function with an invalid directory path, with check and with recursive."""
    mocker.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=argparse.Namespace(
            path=invalid_format_dir_subdirs,
            recursive=True,
            check=True,
            diff=False,
            color=False,
            sort_keys=False,
            indent=None,
            tab=False,
            no_indent=False,
            compact=False,
        ),
    )
    assert main() == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value
