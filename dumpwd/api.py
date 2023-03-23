import os
import fnmatch
import textwrap
from typing import List, Union, Tuple
import fnmatch


def get_inodes(
    path: str,
    exclude: Union[str, List[str]] = None,
    read_files: bool = True,
    max_depth: int = -1,
) -> List[Tuple[str, Union[str, List]]]:
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

    def dfs(directory: str, depth: int) -> List[Tuple[str, Union[str, List]]]:
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


from typing import List, Tuple, Union
from contextlib import redirect_stdout
from io import StringIO
import os


def get_tree(
    inodes: List[Tuple[str, Union[str, List]]],
    prefix: str = "",
    max_depth: int = None,
    current_depth: int = 0,
) -> str:
    if max_depth is not None and current_depth > max_depth:
        return ""

    space = "    "
    branch = "│   "
    tee = "├── "
    last = "└── "
    for i, (name, contents) in enumerate(inodes):
        is_last = i == len(inodes) - 1
        if isinstance(contents, list):
            # Directory
            print(f"{prefix}{last if is_last else tee}{name}")
            new_prefix = prefix + (space if is_last else branch)
            get_tree(contents, new_prefix, max_depth, current_depth + 1)
        else:
            # File
            print(f"{prefix}{last if is_last else tee}{name}")


def get_files(
    inodes: List[Tuple[str, Union[str, List]]],
    path: str = "",
    max_depth: int = None,
    current_depth: int = 0,
) -> str:
    if max_depth is not None and current_depth > max_depth:
        return

    def print_file_contents(file_path: str, contents: str):
        print(f"# {file_path}:\n```\n{contents}\n```\n\n")

    for name, contents in inodes:
        current_path = os.path.join(path, name)
        if isinstance(contents, list):
            # Directory
            print(
                f"{current_path}: {', '.join([entry[0] for entry in contents if not isinstance(entry[1], list)])}"
            )
            get_files(contents, current_path, max_depth, current_depth + 1)
        else:
            # File
            if contents is not None:
                print_file_contents(current_path, contents)
