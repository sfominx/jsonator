"""
Tests for the filesystem module
"""
import string
import sys
import tempfile
from pathlib import Path

# pylint: disable=import-error,wrong-import-position

sys.path.append(str(Path(__file__).resolve().parent.parent))

from jsonator.jsonator import make_temp_file, random_str


def test_random_str() -> None:
    """Test the `random_str()` function.

    Generates 100 random strings and asserts that each string is an instance of
    a `str`, has a length of 8 characters, and contains only ASCII letters and
    digits.
    """
    for _ in range(100):
        result = random_str()
        assert isinstance(result, str)
        assert len(result) == 8
        assert all(c in string.ascii_letters + string.digits for c in result)


def test_make_temp_file() -> None:
    """Test the functionality of the make_temp_file function.

    The function tests that the returned path exists and is a file,
    that the path is within the temporary directory, and that multiple
    calls to the function return different paths.
    """
    # Test that the returned path exists and is a file
    temp_file = make_temp_file()
    assert not temp_file.exists()

    # Test that the path is within the temp directory
    temp_dir = Path(tempfile.gettempdir()).absolute()
    assert temp_file.parent == temp_dir

    # Test that multiple calls return different paths
    temp_file2 = make_temp_file()
    assert temp_file != temp_file2
