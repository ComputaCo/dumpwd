from contextlib import redirect_stdout
from io import StringIO
import json
import math
import os
from pathlib import Path
from typing import List

import typer
from dumpwd.api import get_inodes, get_tree, get_files


def main(
    path: str = typer.Argument(".", help="Path to the directory."),
    exclude: List[str] = typer.Option(
        None, help="List of files or directories to exclude."
    ),
    read_files: bool = typer.Option(
        True, help="If set, print the contents of the files."
    ),
    max_depth: int = typer.Option(None, help="Maximum depth to traverse."),
):
    if max_depth is None:
        max_depth = math.inf

    """
    Print the file system tree at the given path (default is the current working directory) and optionally print the contents of the files.

    If `read_files` is set, the contents of the files will also be printed.
    """
    # Get the contents
    inodes = get_inodes(path, exclude=exclude, read_files=read_files, max_depth=max_depth)

    # Print the tree
    get_tree(inodes, prefix="", max_depth=max_depth)

    # Print the file contents if `read_files` is set
    get_files(inodes, path=path, max_depth=max_depth)


if __name__ == "__main__":
    typer.run(main)
