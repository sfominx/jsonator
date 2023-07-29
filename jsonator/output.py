"""
Output features
"""


def diff(a_text: str, b_text: str, a_name: str, b_name: str) -> str:
    """Return a unified diff string between strings `a` and `b`."""
    import difflib  # pylint: disable=import-outside-toplevel

    a_lines = a_text.splitlines(keepends=True)
    b_lines = b_text.splitlines(keepends=True)
    diff_lines = []
    for line in difflib.unified_diff(a_lines, b_lines, fromfile=a_name, tofile=b_name, n=5):
        # Work around https://bugs.python.org/issue2142
        # See:
        # https://www.gnu.org/software/diffutils/manual/html_node/Incomplete-Lines.html
        if line[-1] == "\n":
            diff_lines.append(line)
        else:
            diff_lines.append(line + "\n")
            diff_lines.append("\\ No newline at end of file\n")
    return "".join(diff_lines)


def color_diff(contents: str) -> str:
    """Inject the ANSI color codes to the diff."""
    lines = contents.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("+++") or line.startswith("---"):
            line = "\033[1m" + line + "\033[0m"  # bold, reset
        elif line.startswith("@@"):
            line = "\033[36m" + line + "\033[0m"  # cyan, reset
        elif line.startswith("+"):
            line = "\033[32m" + line + "\033[0m"  # green, reset
        elif line.startswith("-"):
            line = "\033[31m" + line + "\033[0m"  # red, reset
        lines[i] = line
    return "\n".join(lines)
