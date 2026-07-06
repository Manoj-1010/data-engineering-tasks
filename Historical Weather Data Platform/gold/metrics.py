from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    avg,
    sum,
)


def build_city_year_weather_summary(
    silver_df: DataFrame,
) -> DataFrame:
    """
    Yearly weather summary per city.
    """

    return (
        silver_df
        .groupBy(
            "city",
            "year"
        )
        .agg(
            avg("temperature_mean").alias(
                "average_temperature"
            ),
            sum("precipitation").alias(
                "total_precipitation"
            ),
            avg("relative_humidity").alias(
                "average_humidity"
            ),
            avg("cloud_cover").alias(
                "average_cloud_cover"
            ),
            avg("wind_speed_mean").alias(
                "average_wind_speed"
            ),
        )
        .orderBy(
            "city",
            "year"
        )
    )


def build_city_month_weather_summary(
    silver_df: DataFrame,
) -> DataFrame:
    """
    Monthly weather summary per city.
    Useful for trend analysis.
    """

    return (
        silver_df
        .groupBy(
            "city",
            "year",
            "month"
        )
        .agg(
            avg("temperature_mean").alias(
                "average_temperature"
            ),
            sum("precipitation").alias(
                "total_precipitation"
            ),
            avg("relative_humidity").alias(
                "average_humidity"
            ),
            avg("cloud_cover").alias(
                "average_cloud_cover"
            ),
        )
        .orderBy(
            "city",
            "year",
            "month"
        )
    )