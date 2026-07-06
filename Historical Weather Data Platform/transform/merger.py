from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, coalesce


JOIN_COLUMNS = [
    "city",
    "date",
]


COMMON_COLUMNS = [
    "temperature_mean",
    "temperature_max",
    "temperature_min",
    "precipitation",
    "relative_humidity",
    "cloud_cover",
    "shortwave_radiation",
]


OPENMETEO_ONLY_COLUMNS = [
    "weather_code",
    "apparent_temperature",
    "rain_sum",
    "snowfall_sum",
    "precipitation_hours",
    "wind_speed_mean",
    "wind_speed_max",
    "wind_gusts_max",
    "wind_direction",
    "pressure_msl",
    "sunshine_duration",
    "sunrise",
    "sunset",
    "daylight_duration",
    "time_zone",
]


NASA_ONLY_COLUMNS = [
    "dew_point_temperature",
    "surface_pressure",
    "surface_temperature",
]


METADATA_COLUMNS = [
    "year",
    "month",
]


def merge_weather_data(
    openmeteo_df: DataFrame,
    nasa_df: DataFrame,
) -> DataFrame:
    """
    Merge the transformed Open-Meteo and NASA POWER datasets.

    Open-Meteo is considered the primary source.

    NASA POWER fills missing values whenever possible.
    """

    om = openmeteo_df.alias("om")
    np = nasa_df.alias("np")

    joined = om.join(
        np,
        on=JOIN_COLUMNS,
        how="full_outer",
    )

    columns = []

    # Join columns
    columns.extend(
        col(column)
        for column in JOIN_COLUMNS
    )

    # Metadata
    columns.extend(
        coalesce(
            col(f"om.{column}"),
            col(f"np.{column}")
        ).alias(column)
        for column in METADATA_COLUMNS
    )

    # Shared weather columns
    columns.extend(
        coalesce(
            col(f"om.{column}"),
            col(f"np.{column}")
        ).alias(column)
        for column in COMMON_COLUMNS
    )

    # OpenMeteo exclusive
    columns.extend(
        col(f"om.{column}").alias(column)
        for column in OPENMETEO_ONLY_COLUMNS
    )

    # NASA exclusive
    columns.extend(
        col(f"np.{column}").alias(column)
        for column in NASA_ONLY_COLUMNS
    )

    return joined.select(*columns)