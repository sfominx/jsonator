"""Pytest fixtures."""
import sys
from pathlib import Path

import pytest

FILES_ENCODING = "utf-8"
INTERPRETER = Path(sys.executable).stem


@pytest.fixture
def valid_format_json(tmp_path: Path) -> Path:
    """Create a temporary file for testing with valid json formatting"""
    file_path = tmp_path / "test.json"
    file_path.write_text('{\n    "key": "value"\n}\n', encoding=FILES_ENCODING)
    return file_path


@pytest.fixture
def valid_format_dir_no_subdirs(tmp_path: Path) -> Path:
    """Create a temporary file for testing with valid json formatting"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True)
    file_path = test_dir / "test1.json"
    file_path.write_text('{\n    "key": "value1"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test2.json"
    file_path.write_text('{\n    "key": "value2"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test3.json"
    file_path.write_text('{\n    "key": "value3"\n}\n', encoding=FILES_ENCODING)
    return test_dir


@pytest.fixture
def valid_format_dir_subdirs(tmp_path: Path) -> Path:
    """Create a temporary file for testing with valid json formatting"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True)
    test_subdir = test_dir / "test_subdir"
    test_subdir.mkdir(parents=True)
    file_path = test_subdir / "test1.json"
    file_path.write_text('{\n    "key": "value1"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test2.json"
    file_path.write_text('{\n    "key": "value2"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test3.json"
    file_path.write_text('{\n    "key": "value3"\n}\n', encoding=FILES_ENCODING)
    return test_dir


@pytest.fixture
def invalid_format_json(tmp_path: Path) -> Path:
    """Create a temporary file for testing with invalid json formatting"""
    file_path = tmp_path / "test_incorrect.json"
    file_path.write_text('{"key": "value"}', encoding=FILES_ENCODING)
    return file_path

@pytest.fixture
def invalid_format_json_multiple_keys(tmp_path: Path) -> Path:
    """Create a temporary file for testing
    with invalid json formatting and multiple keys"""
    file_path = tmp_path / "test_incorrect.json"
    file_path.write_text('{"key2": "value", "key1": "value2"}', encoding=FILES_ENCODING)
    return file_path

@pytest.fixture
def invalid_format_dir_no_subdirs(tmp_path: Path) -> Path:
    """Create a temporary file for testing with valid json formatting"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True)
    file_path = test_dir / "test1.json"
    file_path.write_text('{\n    "key": "value1"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test2.json"
    file_path.write_text('{\n    "key": "value2"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test3.json"
    file_path.write_text('{"key": "value3"}', encoding=FILES_ENCODING)
    return test_dir


@pytest.fixture
def invalid_format_dir_subdirs(tmp_path: Path) -> Path:
    """Create a temporary file for testing with valid json formatting"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True)
    test_subdir = test_dir / "test_subdir"
    test_subdir.mkdir(parents=True)
    file_path = test_subdir / "test1.json"
    file_path.write_text('{\n    "key": "value1"\n}\n', encoding=FILES_ENCODING)
    file_path = test_dir / "test2.json"
    file_path.write_text('{\n    "key": "value2"\n}\n', encoding=FILES_ENCODING)
    file_path = test_subdir / "test3.json"
    file_path.write_text('{"key": "value3"}', encoding=FILES_ENCODING)
    return test_dir


@pytest.fixture
def invalid_json(tmp_path: Path) -> Path:
    """Create a temporary file for testing with invalid json formatting"""
    file_path = tmp_path / "test_invalid.json"
    file_path.write_text('{"', encoding=FILES_ENCODING)
    return file_path


@pytest.fixture
def invalid_json_in_dir(tmp_path: Path) -> Path:
    """Create a temporary file inside directory for testing with invalid json formatting"""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir(parents=True)
    file_path = test_dir / "test_invalid.json"
    file_path.write_text('{"', encoding=FILES_ENCODING)
    return file_path
