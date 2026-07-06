import json
from pathlib import Path
from typing import Any

from pyspark.sql import DataFrame


def ensure_directory(path: Path) -> None:
    """
    Create a directory if it does not exist.
    """

    path.mkdir(
        parents=True,
        exist_ok=True
    )


def write_json(
    path: Path,
    data: Any
) -> None:
    """
    Write JSON to disk.
    """

    ensure_directory(path.parent)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=4
        )


def write_parquet(
    df: DataFrame,
    output_path: str,
    partition_by: list[str] | None = None,
    mode: str = "overwrite"
) -> None:
    """
    Write a Spark DataFrame as Parquet.

    Parameters
    ----------
    df
        Spark DataFrame

    output_path
        Destination path

    partition_by
        Columns to partition by

    mode
        Spark write mode
    """

    writer = df.write.mode(mode)

    if partition_by:
        writer.partitionBy(*partition_by)

    writer.parquet(output_path)