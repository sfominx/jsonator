"""
Summarize runs.
"""

import logging
from pathlib import Path

from jsonator.enum import ReturnCode


class Report:
    """Provides a reformatting counter. Can be rendered with `str(report)`."""

    def __init__(self, check: bool, diff: bool) -> None:
        self.check = check
        self.diff = diff
        self.change_count = 0
        self.same_count = 0
        self.failure_count = 0
        self._log = logging.getLogger(self.__class__.__name__)

    def done(self, src: Path, changed: bool) -> None:
        """Increment the counter for successful reformatting. Write out a message."""
        if changed:
            reformatted = "would reformat" if self.check or self.diff else "reformatted"
            self._log.warning("%s %s", reformatted, src)
            self.change_count += 1

        else:
            self._log.info("%s already well formatted, good job.", src)
            self.same_count += 1

    def failed(self, src: Path, message: str) -> None:
        """Increment the counter for failed reformatting. Write out a message."""
        self._log.error("error: cannot format %s: %s", src, message)
        self.failure_count += 1

    @property
    def status(self) -> int:
        """Return the exit code that the app should use.

        This considers the current state of changed files and failures:
        - if there were any failures, return 123;
        - if any files were changed and --check is being used, return 1;
        - otherwise return 0.
        """
        if self.failure_count:
            return ReturnCode.INTERNAL_ERROR.value

        if self.change_count and self.check:
            return ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value

        return ReturnCode.NOTHING_WOULD_CHANGE.value

    def __str__(self) -> str:
        """Render a report of the current state."""
        if self.check or self.diff:
            reformatted = "would be reformatted"
            unchanged = "would be left unchanged"
            failed = "would fail to reformat"

        else:
            reformatted = "reformatted"
            unchanged = "left unchanged"
            failed = "failed to reformat"

        report = []

        if self.change_count:
            report.append(f"{self.change_count} file{'s'[:self.change_count ^ 1]} {reformatted}")

        if self.same_count:
            report.append(f"{self.same_count} file{'s'[:self.same_count ^ 1]} {unchanged}")

        if self.failure_count:
            report.append(f"{self.failure_count} file{'s'[:self.failure_count ^ 1]} {failed}")

        return ", ".join(report) + "."
