"""Main function"""
import argparse
import sys
from pathlib import Path

from jsonator.enum import ReturnCode
from jsonator.jsonator import format_json_file
from jsonator.report import Report


def main() -> int:
    """Main function"""
    arg_parser = argparse.ArgumentParser(
        prog="jsonator", formatter_class=argparse.RawTextHelpFormatter
    )
    arg_parser.add_argument("path", type=Path, help="Path to the JSON file or directory")
    arg_parser.add_argument("--recursive", "-r", action="store_true", help="Scan subdirectories")
    arg_parser.add_argument(
        "--check",
        action="store_true",
        help="""Don't write the files back, just return the status.
Return code 0 means nothing would change. 
Return code 1 means some files would be reformatted.
Return code 122 means file not found.
Return code 123 means there was an internal error.""",
    )
    arg_parser.add_argument(
        "--diff",
        action="store_true",
        help="Don't write the files back, just output a diff for each file on stdout.",
    )
    arg_parser.add_argument(
        "--color",
        action="store_true",
        help="Show colored diff. Only applies when `--diff` is given.",
    )
    arg_parser.add_argument(
        "--sort-keys",
        action="store_true",
        help="Sort the output of dictionaries alphabetically by key.",
    )
    arg_parser.add_argument(
        "--no-ensure-ascii",
        action="store_true",
        help="Disable escaping of non-ASCII characters.",
    )
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--indent",
        type=int,
        help="Separate items with newlines and use this number of spaces for indentation.",
    )
    group.add_argument(
        "--tab",
        action="store_true",
        help="Separate items with newlines and use tabs for indentation.",
    )
    group.add_argument(
        "--no-indent", action="store_true", help="Separate items with spaces rather than newlines."
    )
    group.add_argument(
        "--compact", action="store_true", help="Suppress all whitespace separation (most compact)."
    )

    args = arg_parser.parse_args()

    if not args.path.exists():
        return ReturnCode.FILE_NOT_FOUND.value

    if args.sort_keys and sys.version_info < (3, 5):
        print("The `--sort-keys` option is only available on Python 3.5 and above", file=sys.stderr)
        return ReturnCode.INTERNAL_ERROR.value
    forbidden_python39_args = (
        args.indent or args.tab or args.no_indent or args.tab or args.no_ensure_ascii
    )
    if forbidden_python39_args and sys.version_info < (3, 9):
        print(
            "`--indent`, `--tab`, `--no-indent`, `--compact` options "
            "are only available on Python 3.9 and above",
            file=sys.stderr,
        )
        return ReturnCode.INTERNAL_ERROR.value

    report = Report(args.check, args.diff)

    if args.path.is_dir():
        pattern = "**/*.json" if args.recursive else "*.json"
        files_to_scan = list(args.path.glob(pattern))

    else:
        files_to_scan = [
            args.path,
        ]

    for file_to_scan in files_to_scan:
        format_json_file(
            file_to_scan,
            report,
            args.check,
            args.diff,
            args.color,
            args.sort_keys,
            args.indent,
            args.tab,
            args.no_indent,
            args.compact,
            args.no_ensure_ascii,
        )

    print(report)
    return report.status
