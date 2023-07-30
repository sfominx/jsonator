"""Main function"""
import argparse
import sys
from pathlib import Path

from jsonator.jsonator import ReturnCode, format_json_file


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

    args = arg_parser.parse_args()

    if not args.path.exists():
        return ReturnCode.FILE_NOT_FOUND.value

    if args.sort_keys and sys.version_info < (3, 5):
        print("The `--sort-keys` option is only available on Python 3.5 and above", file=sys.stderr)
        return ReturnCode.INTERNAL_ERROR.value

    if args.path.is_dir():
        all_files_identical = True
        pattern = "**/*.json" if args.recursive else "*.json"

        for json_file in args.path.glob(pattern):
            result = format_json_file(json_file, args.check, args.diff, args.color, args.sort_keys)

            if result == ReturnCode.INTERNAL_ERROR:
                return ReturnCode.INTERNAL_ERROR.value

            if result == ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED and args.check:
                all_files_identical = False

        return (
            ReturnCode.NOTHING_WOULD_CHANGE.value
            if all_files_identical
            else ReturnCode.SOME_FILES_WOULD_BE_REFORMATTED.value
        )

    return format_json_file(args.path, args.check, args.diff, args.color, args.sort_keys).value
