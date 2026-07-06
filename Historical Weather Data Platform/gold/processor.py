from pathlib import Path

from pyspark.sql import SparkSession

from common.base import BasePipeline
from common.writer import write_parquet

from gold.metrics import (
    build_city_year_weather_summary,
    build_city_month_weather_summary,
)


class GoldProcessor(BasePipeline):

    def __init__(
        self,
        spark: SparkSession,
    ) -> None:

        super().__init__()

        self.spark = spark

    def run(self) -> None:

        silver_df = self.spark.read.parquet(
            self.config[
                "silver_storage_base_path"
            ]
        )

        city_year_weather_summary = (
            build_city_year_weather_summary(
                silver_df
            )
        )

        city_month_weather_summary = (
            build_city_month_weather_summary(
                silver_df
            )
        )

        gold_base_path = Path(
            self.config[
                "gold_storage_base_path"
            ]
        )

        write_parquet(
            df=city_year_weather_summary,
            output_path=str(
                gold_base_path
                / "city_year_weather_summary"
            ),
        )

        write_parquet(
            df=city_month_weather_summary,
            output_path=str(
                gold_base_path
                / "city_month_weather_summary"
            ),
        )