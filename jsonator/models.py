"""Models"""

from dataclasses import dataclass


@dataclass
class ModeArgs:
    """Mode args"""

    check: bool
    diff: bool
    color: bool
