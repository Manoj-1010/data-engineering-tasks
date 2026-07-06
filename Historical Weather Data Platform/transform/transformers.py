from __future__ import annotations

import pandas as pd

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col,
    date_format,
    lit,
    month,
    to_date,
    year,
)

from WDataSchemas import (
    OPENMETEO_SCHEMA,
    NASAPOWER_SCHEMA,
)

from transform.mappings import (
    OPENMETEO_COLUMN_MAPPINGS,
    NASAPOWER_COLUMN_MAPPINGS,
)


def rename_columns(
    df: DataFrame,
    mappings: dict[str, str],
) -> DataFrame:
    """
    Rename dataframe columns according to the supplied mapping.
    """

    return df.select(
        *[
            col(column).alias(
                mappings.get(column, column)
            )
            for column in df.columns
        ]
    )


def transform_openmeteo(
    spark: SparkSession,
    json_data: dict,
    city: str,
) -> DataFrame:
    """
    Transform an Open-Meteo response into the project's
    canonical schema.
    """

    pdf = pd.DataFrame(
        json_data["daily"]
    )

    pdf["weather_code"] = (
        pd.to_numeric(
            pdf["weather_code"],
            errors="coerce",
        )
        .astype("Int64")
    )

    numeric_columns = [
        column
        for column in pdf.columns
        if column not in {
            "time",
            "sunrise",
            "sunset",
            "weather_code",
        }
    ]

    pdf[numeric_columns] = (
        pdf[numeric_columns]
        .apply(
            pd.to_numeric,
            errors="coerce",
        )
        .astype("float64")
    )

    sdf = spark.createDataFrame(
        pdf,
        schema=OPENMETEO_SCHEMA,
    )

    sdf = rename_columns(
        sdf,
        OPENMETEO_COLUMN_MAPPINGS,
    )

    return (
        sdf
        .withColumn(
            "time_zone",
            lit(
                json_data[
                    "timezone_abbreviation"
                ]
            ),
        )
        .withColumn(
            "city",
            lit(city),
        )
        .withColumn(
            "year",
            year(col("date")),
        )
        .withColumn(
            "month",
            month(col("date")),
        )
    )


def transform_nasapower(
    spark: SparkSession,
    json_data: dict,
    city: str,
) -> DataFrame:
    """
    Transform a NASA POWER response into the project's
    canonical schema.
    """

    pdf = pd.DataFrame(
        json_data["properties"]["parameter"]
    )

    pdf = (
        pdf
        .reset_index()
        .rename(
            columns={
                "index": "date"
            }
        )
    )

    sdf = spark.createDataFrame(
        pdf,
        schema=NASAPOWER_SCHEMA,
    )

    sdf = rename_columns(
        sdf,
        NASAPOWER_COLUMN_MAPPINGS,
    )

    sdf = (
        sdf
        .withColumn(
            "date",
            date_format(
                to_date(
                    col("date").cast("string"),
                    "yyyyMMdd",
                ),
                "yyyy-MM-dd",
            ),
        )
        .withColumn(
            "city",
            lit(city),
        )
        .withColumn(
            "year",
            year(col("date")),
        )
        .withColumn(
            "month",
            month(col("date")),
        )
    )

    return sdf