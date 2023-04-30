from contextlib import redirect_stdout
from io import StringIO
import os


def get_tree(
    inodes: list[tuple[str, str | list]],
    prefix: str = "",
    depth: int = None,
    current_depth: int = 0,
) -> str:
    """
    Recursively retrieves the directory tree rooted at the given path.

    :param inodes: A list of tuples representing the inodes of the directory tree.
    :param prefix: A string indicating the prefix to use for each line in the output.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse.
    :param current_depth: An integer indicating the current depth in the directory tree.
    :return: A string containing the directory tree.
    """
    if depth is not None and current_depth > depth:
        return ""

    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "

    output = ""

    for i, (name, contents) in enumerate(inodes):
        is_last = i == len(inodes) - 1
        if isinstance(contents, list):
            # Directory
            output += f"{prefix}{last if is_last else tee}{name}\n"
            new_prefix = prefix + (space if is_last else branch)
            output += get_tree(contents, new_prefix, depth, current_depth + 1)
        else:
            # File
            output += f"{prefix}{last if is_last else tee}{name}\n"

    return output + "\n"
