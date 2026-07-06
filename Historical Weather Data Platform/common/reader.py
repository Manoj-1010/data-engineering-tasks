import json
from pathlib import Path
from typing import Any, Generator


def read_json(path: Path) -> dict[str, Any]:
    """
    Read a JSON file.
    """

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def iter_files(
    root: Path,
    pattern: str = "*.json"
) -> Generator[Path, None, None]:
    """
    Recursively yield files matching a pattern.

    Example
    -------
    >>> for file in iter_files(Path("./bronze")):
    """

    yield from root.rglob(pattern)