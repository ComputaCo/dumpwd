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

import dumpwd.api as api
import dumpwd._internal.consts as consts


# @app.callback(invoke_without_command=True)
# def main(
#     path: Optional[str] = typer.Argument("."),
#     exclude: list[str] = typer.Option(
#         consts.IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
#     ),
#     read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
#     depth: Optional[int] = typer.Option(
#         None, help="Depth of directories to traverse. 0=only top-level"
#     ),
#     prefix: str = "",
#     # help: bool = typer.Option(False, "--help", "-h", help="Show this help message."),
# ):
#     inodes = api.get_inodes(path, exclude=exclude, read=read, depth=depth)
#     typer.echo(api.get_tree(inodes, prefix=prefix, depth=depth))
#     typer.echo(api.get_contents(inodes, path=path, depth=depth))
#     raise typer.Exit()


@app.command()
def get_inodes(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        consts.IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
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
    inodes = api.get_inodes(path, exclude=exclude, read=read, depth=depth)
    typer.echo(inodes)
    raise typer.Exit()


@app.command()
def get_tree(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        consts.IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
    ),
    read: bool = typer.Option(True, help="Whether to read the files that are traversed"),
    depth: Optional[int] = typer.Option(
        None, help="Depth of directories to traverse. 0=only top-level"
    ),
    prefix: str = "",
    compressed: bool = typer.Option(
        False, "--compressed", "-c", help="Compressed output."
    ),
):
    """
    This command retrieves the directory tree rooted at the given path.

    :param path: The root path of the directory tree. Default is ".".
    :param exclude: A list of strings containing patterns of paths to exclude. Default is None.
    :param read: A boolean indicating whether to read the contents of the files. Default is True.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse. Default is None.
    :param prefix: A string indicating the prefix to use for each line in the output. Default is an empty string.
    :param compressed: A boolean indicating whether to compress the output. Default is False.
    """
    inodes = api.get_inodes(path, exclude=exclude, read=read, depth=depth)
    typer.echo(api.get_tree(inodes, prefix=prefix, depth=depth, compressed=compressed))
    raise typer.Exit()


@app.command()
def get_contents(
    path: Optional[str] = typer.Argument("."),
    exclude: list[str] = typer.Option(
        consts.IGNORE_PREFIXES, "--exclude", "-e", help="Patterns of paths to exclude."
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
    inodes = api.get_inodes(path, exclude=exclude, read=read, depth=depth)
    typer.echo(api.get_contents(inodes, path=path, depth=depth))
    raise typer.Exit()
