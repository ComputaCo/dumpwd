import fnmatch
import math
import os

from dumpwd._consts import IGNORE_PREFIXES


def get_inodes(
    path: str,
    exclude: str | list[str] = IGNORE_PREFIXES,
    read_files: bool = True,
    depth: int = None,
) -> list[tuple[str, str | list]]:
    """
    Recursively retrieves the inodes of the directory tree rooted at the given path.

    :param path: The root path of the directory tree.
    :param exclude: A string or list of strings containing patterns of paths to exclude.
    :param read_files: A boolean indicating whether to read the contents of the files.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse.
    :return: A list of tuples representing the inodes of the directory tree.
    """
    max_depth = depth or -1  # -1 indicates no limit on mo
    del depth

    if isinstance(exclude, str):
        exclude = [exclude]
    elif exclude is None:
        exclude = []

    def is_excluded(file: str) -> bool:
        for pattern in exclude:
            if fnmatch.fnmatch(file, pattern):
                return True
        return False

    def is_text(file: str) -> bool:
        try:
            with open(file, "tr") as f:
                f.read(1)
            return True
        except UnicodeDecodeError:
            return False

    def dfs(directory: str, depth: int) -> list[tuple[str, str | list]]:
        if depth == 0:
            return []
        inodes = []
        for entry in os.scandir(directory):
            if is_excluded(entry.name):
                continue
            if entry.is_file():
                if not is_text(entry.path):
                    continue
                contents = None
                if read_files:
                    with open(entry.path, "r") as f:
                        contents = f.read()
                inodes.append((entry.name, contents))
            elif entry.is_dir():
                inodes.append((entry.name, dfs(entry.path, depth - 1)))

        # sort inodes
        inodes.sort(key=lambda x: x[0])
        return inodes

    return dfs(path, max_depth)
