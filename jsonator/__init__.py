"""Main function"""

import argparse
from pathlib import Path

from jsonator.enum import ReturnCode
from jsonator.jsonator import format_json_file
from jsonator.models import ModeArgs
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
        default=False,
        help="""Don't write the files back, just return the status.
Return code 0 means nothing would change.
Return code 1 means some files would be reformatted.
Return code 122 means file not found.
Return code 123 means there was an internal error.""",
    )
    arg_parser.add_argument(
        "--diff",
        action="store_true",
        default=False,
        help="Don't write the files back, just output a diff for each file on stdout.",
    )
    arg_parser.add_argument(
        "--color",
        action="store_true",
        default=False,
        help="Show colored diff. Only applies when `--diff` is given.",
    )
    arg_parser.add_argument(
        "--sort-keys",
        action="store_true",
        default=False,
        help="Sort the output of dictionaries alphabetically by key.",
    )
    arg_parser.add_argument(
        "--no-ensure-ascii",
        dest="ensure_ascii",
        action="store_false",
        help="Disable escaping of non-ASCII characters.",
    )
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument(
        "--indent",
        type=int,
        default=4,
        help="Separate items with newlines and use this number of spaces for indentation.",
    )
    group.add_argument(
        "--tab",
        dest="indent",
        action="store_const",
        const="\t",
        help="Separate items with newlines and use tabs for indentation.",
    )
    group.add_argument(
        "--no-indent",
        dest="indent",
        action="store_const",
        const=None,
        help="Separate items with spaces rather than newlines.",
    )
    group.add_argument(
        "--compact", action="store_true", help="Suppress all whitespace separation (most compact)."
    )

    args = arg_parser.parse_args()

    if not args.path.exists():
        return ReturnCode.FILE_NOT_FOUND.value

    dump_args = {
        "sort_keys": args.sort_keys,
        "indent": args.indent,
        "ensure_ascii": args.ensure_ascii,
    }

    if args.compact:
        dump_args["indent"] = None
        dump_args["separators"] = ",", ":"

    report = Report(args.check, args.diff)

    if args.path.is_dir():
        pattern = "**/*.json" if args.recursive else "*.json"
        files_to_scan = list(args.path.glob(pattern))

    else:
        files_to_scan = [
            args.path,
        ]
    mode_args = ModeArgs(args.check, args.diff, args.color)
    for file_to_scan in files_to_scan:
        format_json_file(file_to_scan, report, mode_args, dump_args)

    return report.status
