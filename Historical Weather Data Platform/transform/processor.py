from __future__ import annotations

from functools import reduce
from pathlib import Path

from pyspark.sql import SparkSession, DataFrame

from common.base import BasePipeline
from common.reader import read_json
from common.writer import write_parquet

from transform.transformers import (
    transform_openmeteo,
    transform_nasapower,
)

from transform.merger import merge_weather_data


class WeatherDataProcessor(BasePipeline):
    """
    Convert Bronze weather data into a unified Silver dataset.
    """

    def __init__(
        self,
        spark: SparkSession,
    ) -> None:

        super().__init__()

        self.spark = spark

    def _read_openmeteo(
        self,
        city: str,
        year: int,
    ) -> dict:

        path = (
            Path(
                self.config["openmeteo_bronze_storage_base_path"]
            )
            / city
            / str(year)
            / f"{city}_{year}.json"
        )

        return read_json(path)

    def _read_nasa(
        self,
        city: str,
        year: int,
    ) -> dict:

        path = (
            Path(
                self.config["nasapower_bronze_storage_base_path"]
            )
            / city
            / str(year)
            / f"{city}_{year}.json"
        )

        return read_json(path)

    def run(self) -> None:

        merged_dataframes: list[DataFrame] = []

        for city in self.config["cities"]:

            for year in range(
                self.config["start_year"],
                self.config["end_year"] + 1,
            ):

                openmeteo_json = self._read_openmeteo(
                    city,
                    year,
                )

                nasa_json = self._read_nasa(
                    city,
                    year,
                )

                openmeteo_df = transform_openmeteo(
                    self.spark,
                    openmeteo_json,
                    city,
                )

                nasa_df = transform_nasapower(
                    self.spark,
                    nasa_json,
                    city,
                )

                silver_df = merge_weather_data(
                    openmeteo_df,
                    nasa_df,
                )

                merged_dataframes.append(
                    silver_df
                )

        final_df = reduce(
            lambda left, right: left.unionByName(right),
            merged_dataframes,
        )

        write_parquet(
            df=final_df,
            output_path=self.config[
                "silver_storage_base_path"
            ],
            partition_by=["year"],
        )


if __name__ == "__main__":

    spark = (
        SparkSession.builder
        .appName("Weather Silver Processor")
        .getOrCreate()
    )

    WeatherDataProcessor(
        spark
    ).run()

    spark.stop()