import os


def get_contents(
    inodes: list[tuple[str, str | list]],
    path: str = "",
    depth: int = None,
    current_depth: int = 0,
) -> str:
    """
    Recursively retrieves the contents of the directory tree rooted at the given path.

    :param inodes: A list of tuples representing the inodes of the directory tree.
    :param path: The path to the root of the directory tree.
    :param depth: An integer indicating the maximum depth of the directory tree to traverse.
    :param current_depth: An integer indicating the current depth in the directory tree.
    :return: A string containing the contents of the directory tree.
    """
    if depth is not None and current_depth > depth:
        return

    output = ""

    def print_file_contents(file_path: str, contents: str):
        nonlocal output
        output += f"# {file_path}:\n```\n{contents}\n```\n\n"

    for name, contents in inodes:
        current_path = os.path.join(path, name)
        if isinstance(contents, list):
            # Directory
            output += f"{current_path}: {', '.join([entry[0] for entry in contents if not isinstance(entry[1], list)])}\n"
            get_contents(contents, current_path, depth, current_depth + 1)
        else:
            # File
            if contents is not None:
                print_file_contents(current_path, contents)
