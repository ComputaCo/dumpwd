from typing import Optional
import typer
from contextlib import redirect_stdout
from io import StringIO
import json
import math
import os
from pathlib import Path
import pprint

app = typer.Typer(add_completion=False)
pp = pprint.PrettyPrinter(indent=4)

from dumpwd._get_inodes import get_inodes as _get_inodes
from dumpwd._get_tree import get_tree as _get_tree
from dumpwd._get_contents import get_contents as _get_contents
from dumpwd._consts import IGNORE_PREFIXES


@app.callback(invoke_without_command=True)
def main(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
    ),
    read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
    depth: Optional[int] = typer.Option(
        None, help="Depth of directories to traverse. 0=only top-level"
    ),
    prefix: str = "",
):
    pass
    # inodes = _get_inodes(path, exclude=exclude, read=read, depth=depth)
    # typer.echo(_get_tree(inodes, prefix=prefix, depth=depth))
    # typer.echo(_get_contents(inodes, path=path, depth=depth))


@app.command()
def get_inodes(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
    ),
    read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
    depth: Optional[int] = typer.Option(
        None, help="Depth of directories to traverse. 0=only top-level"
    ),
):
    """
    This command retrieves the inodes of the directory tree rooted at the given path.

    :param path: The root path of the directory tree.
    :param exclude: A list of strings containing patterns of paths to exclude. Default is None.
    :param read: A boolean indicating whether to read the contents of the files. Default is True.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse. Default is None.
    """
    pp.pprint(_get_inodes(path, exclude=exclude, read=read, depth=depth))


@app.command()
def get_tree(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
    ),
    read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
    depth: Optional[int] = typer.Option(
        None, help="Depth of directories to traverse. 0=only top-level"
    ),
    prefix: str = "",
):
    """
    This command retrieves the directory tree rooted at the given path.

    :param path: The root path of the directory tree. Default is ".".
    :param exclude: A list of strings containing patterns of paths to exclude. Default is None.
    :param read: A boolean indicating whether to read the contents of the files. Default is True.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse. Default is None.
    :param prefix: A string indicating the prefix to use for each line in the output. Default is an empty string.
    """
    inodes = _get_inodes(path, exclude=exclude, read=read, depth=depth)
    typer.echo(_get_tree(inodes, prefix=prefix, depth=depth))


@app.command()
def get_contents(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
    ),
    read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
    depth: Optional[int] = typer.Option(
        None, help="Depth of directories to traverse. 0=only top-level"
    ),
):
    """
    This command retrieves the contents of the directory tree rooted at the given path.

    :param path: The root path of the directory tree. Default is ".".
    :param exclude: A list of strings containing patterns of paths to exclude. Default is None.
    :param read: A boolean indicating whether to read the contents of the files. Default is True.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse. Default is None.
    """
    inodes = _get_inodes(path, exclude=exclude, read=read, depth=depth)
    typer.echo(_get_contents(inodes, path=path, depth=depth))
