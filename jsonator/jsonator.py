"""
Format JSON using json tool
"""
import filecmp
import os
import random
import string
import sys
from enum import Enum
from pathlib import Path
from tempfile import gettempdir

INTERPRETER = Path(sys.executable).stem


class ReturnCode(Enum):
    """Set of possible return codes"""

    NOTHING_WOULD_CHANGE = 0
    SOME_FILES_WOULD_BE_REFORMATTED = 1
    FILE_NOT_FOUND = 122
    INTERNAL_ERROR = 123


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


def format_json_file(json_file: Path, check: bool) -> ReturnCode:
    """
    This function formats the file in JSON format.
    It uses the json.tool module, built into Python, to create a readable JSON format.
    """
    if check:
        print(f"Comparing {json_file} - ", end="")
    else:
        print(f"Formatting {json_file}")

    tmp_file = make_temp_file()
    os.system(f"{INTERPRETER} -m json.tool {json_file} {tmp_file}")

    if check:
        is_identical = filecmp.cmp(json_file, tmp_file, shallow=False)

        if is_identical:
            print("Ok")
            os.unlink(tmp_file)
            return ReturnCode.NOTHING_WOULD_CHANGE

        print("Need to format")
        os.unlink(tmp_file)
        return ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED

    if tmp_file.exists():
        os.unlink(json_file)
        os.rename(tmp_file, json_file)
    else:
        return ReturnCode.INTERNAL_ERROR

    return ReturnCode.NOTHING_WOULD_CHANGE
