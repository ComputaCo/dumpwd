# Technical Spec: dumpwd

## Overview:

`dumpwd` is a Python package that allows the user to dump the contents of a directory tree in a variety of formats. It can be used both as a CLI tool and as an API.

## Installation:

You can install dumpwd using pip:

```
pip install dumpwd
```

## CLI Usage:

The CLI accepts three commands:

1. `get_inodes`: This command retrieves the inodes of the directory tree rooted at the given path.

Example:
```
$ python -m dumpwd get_inodes --exclude "**/venv/**" --read --depth 2 /path/to/dir
```

This command will retrieve the inodes of the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will traverse the directory tree to a maximum depth of 2.

2. `get_tree`: This command retrieves the directory tree rooted at the given path.

Example:
```
$ python -m dumpwd get_tree --exclude "**/venv/**" --read --depth 2 --compressed /path/to/dir
```

This command will retrieve the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will traverse the directory tree to a maximum depth of 2. The output will be compressed.

3. `get_contents`: This command retrieves the contents of the directory tree rooted at the given path.

Example:
```
$ python -m dumpwd get_contents --exclude "**/venv/**" --read --depth 2 /path/to/dir
```

This command will retrieve the contents of the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will traverse the directory tree to a maximum depth of 2.


## API Usage:

The `dumpwd` API provides three functions that correspond to the three CLI commands: `get_inodes()`, `get_tree()`, and `get_contents()`.

1. `get_inodes(path: str, exclude: Union[str, List[str]] = IGNORE_PREFIXES, read: bool = True, depth: Optional[int] = None) -> List[Tuple[str, Union[str, List[Tuple[str, Union[str, List]]]]]]`: This function retrieves the inodes of the directory tree rooted at the given path.

Example:
```python
from dumpwd.api import get_inodes

inodes = get_inodes("/path/to/dir", exclude=["**/venv/**"], read=True, depth=2)
```

This command will retrieve the inodes of the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will traverse the directory tree to a maximum depth of 2.

2. `get_tree(inodes: List[Tuple[str, Union[str, List[Tuple[str, Union[str, List]]]]]], prefix: str = '', depth: Optional[int] = None, current_depth: int = 0, compressed: bool = False) -> str`: This function retrieves the directory tree rooted at the given path.

Example:
```python
from dumpwd.api import get_inodes, get_tree

inodes = get_inodes("/path/to/dir", exclude=["**/venv/**"], read=True, depth=2)
tree = get_tree(inodes, prefix="", depth=None, compressed=False)
```

This command will retrieve the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will traverse the directory tree to a maximum depth of 2. The output will not be compressed.

3. `get_contents(inodes: List[Tuple[str, Union[str, List[Tuple[str, bytes]]]], exclude: Union[str, List[str]] = IGNORE_PREFIXES, read: bool = True) -> List[Tuple[str, bytes]]`: This function retrieves the contents of the directory tree rooted at the given path.

Example:
```python
from dumpwd.api import get_inodes, get_contents

inodes = get_inodes("/path/to/dir", exclude=["**/venv/**"], read=True, depth=2)
contents = get_contents(inodes, exclude=["**/*.txt"], read=True)
```

This command will retrieve the contents of the directory tree rooted at `/path/to/dir`, excluding all directories containing `venv`, and reading the contents of all files. It will exclude all `.txt` files from the contents.

## Contributing

Contributions to this project are welcome and appreciated. To contribute, please follow these steps:

1. Fork the project repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes, and ensure that they work properly.
4. Test your changes thoroughly.
5. Submit a pull request.

Please ensure that your code adheres to the coding standards of the project, and that you have added tests for any new features or changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.