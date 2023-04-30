from contextlib import redirect_stdout
from io import StringIO
import os


def get_tree(
    inodes: list[tuple[str, str | list]],
    prefix: str = "",
    depth: int = None,
    current_depth: int = 0,
    compressed: bool = False,
) -> str:
    """
    Recursively retrieves the directory tree rooted at the given path.

    :param inodes: A list of tuples representing the inodes of the directory tree.
    :param prefix: A string indicating the prefix to use for each line in the output.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse.
    :param current_depth: An integer indicating the current depth in the directory tree.
    :param compressed: A boolean indicating whether to use compressed output.
    :return: A string containing the directory tree.
    """
    if depth is not None and current_depth > depth:
        return ""

    match compressed:
        case True:
            space = "  "
            branch = "│ "
            tee = "├ "
            last = "└ "
        case False:
            space = "    "
            branch = "│   "
            tee = "├── "
            last = "└── "

    with StringIO() as buf, redirect_stdout(buf):

        for i, (name, contents) in enumerate(inodes):
            is_last = i == len(inodes) - 1
            if isinstance(contents, list):
                # Directory
                print(f"{prefix}{last if is_last else tee}{name}")
                new_prefix = prefix + (space if is_last else branch)
                print(
                    get_tree(contents, new_prefix, depth, current_depth + 1, compressed)
                )
            else:
                # File
                print(f"{prefix}{last if is_last else tee}{name}")

        vals = buf.getvalue()
        lines = vals.split("\n")
        liens = filter(lambda line: line.strip(), lines)
        return "\n".join(liens)
