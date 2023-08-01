"""Enums"""
from enum import Enum


class ReturnCode(Enum):
    """Set of possible return codes"""

    NOTHING_WOULD_CHANGE = 0
    SOME_FILES_WOULD_BE_REFORMATTED = 1
    FILE_NOT_FOUND = 122
    INTERNAL_ERROR = 123
