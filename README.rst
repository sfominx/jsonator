JSONator
========

[![Downloads](https://static.pepy.tech/badge/jsonator)](https://pepy.tech/project/jsonator)

Description
-----------

This module provides a command-line interface for formatting JSON files.
It takes a path to either a JSON file or a directory containing JSON files
as input and can recursively scan subdirectories for JSON files. The module
returns an exit code indicating whether any files were reformatted or if there
were any errors.

Usage
-----

The main() function is the entry point for the module and returns an exit code
indicating the result of the JSON formatting operation. The following arguments
can be passed to the main() function:

* path: A required argument that specifies the path to the JSON file or directory containing JSON files to be formatted.

* --recursive or -r: An optional flag that specifies whether to scan subdirectories for JSON files.

* --check: An optional flag that indicates whether to perform a dry run and return the status without actually reformatting the files. The exit code will indicate whether any files would be reformatted or if there were any errors.

* --diff: Don't write the files back, just output a diff for each file on stdout.

* --color: Show colored diff. Only applies when `--diff` is given.

* --sort-keys: Sort the output of dictionaries alphabetically by key.

The module uses the ReturnCode enum to indicate the exit code of the formatting operation. The possible exit codes are:

* `0`: Indicates that no files would be reformatted.

* `1`: Indicates that some files would be reformatted.

* `122`: Indicates that the specified file or directory was not found.

* `123`: Indicates that there was an internal error.

Example usage:
--------------
::

$ jsonator /path/to/json/file.json --check


Dev:
--------------
Build package

::

$ python -m build

Check package

::

$ twine check dist/*

Publish package

::

$ twine upload dist/*