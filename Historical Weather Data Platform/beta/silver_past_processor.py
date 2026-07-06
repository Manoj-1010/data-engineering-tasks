import json
from typing import cast
from pathlib import Path
from pyspark.sql.functions import to_date, col, lit, date_format, year, month
import pandas as pd
import yaml
from tqdm import tqdm
from WDataTypes import WeatherConfig
from WDataSchemas import OPENMETEO_SCHEMA, NASAPOWER_SCHEMA
from column_mappings import OPENMETEO_COLUMN_MAPPINGS, NASAPOWER_COLUMN_MAPPINGS

class WeatherDataProcessor:
    def __init__(self):
        with open("./config.yaml", "r", encoding="utf-8") as file:
            self.config: WeatherConfig = cast(WeatherConfig, yaml.safe_load(file))
        
        self.OPENMETEO_SCHEMA = OPENMETEO_SCHEMA
    
    def _column_mapping(self, sdf, map):
        df= sdf.select(
            *[
                col(c).alias(cast(str, map.get(c, c)))
                for c in sdf.columns
            ]
        )

        return df
    
    def _openmeteo_transformations(self, json_data, city):
        pdf = pd.DataFrame(json_data["daily"])

        pdf["weather_code"] = pd.to_numeric(pdf["weather_code"], errors="coerce").astype("Int64")

        numeric_columns = [
            column
            for column in pdf.columns
            if column not in {"time", "sunrise", "sunset", "weather_code"}
        ]

        pdf[numeric_columns] = pdf[numeric_columns].apply(pd.to_numeric, errors="coerce").astype("float64")

        sdf = spark.createDataFrame(
            pdf,
            schema = self.OPENMETEO_SCHEMA
        )

        sdf = self._column_mapping(sdf, OPENMETEO_COLUMN_MAPPINGS)

        sdf = sdf.withColumn(
            "time_zone",
            lit(json_data["timezone_abbreviation"])
        ).withColumn(
            "city",
            lit(str(city))
        ).withColumn(
            "year",
            year(col("date"))
        ).withColumn(
            "month",
            month(col("date"))
        )

        return sdf
    
    def _nasapower_transformations(self, json_data, city, SCHEMA):
        pdf = pd.DataFrame(json_data["properties"]["parameter"])
        pdf = pdf.reset_index()
        pdf = pdf.rename(columns={"index": "date"})

        sdf = spark.createDataFrame(
            pdf,
            schema = SCHEMA
        )

        sdf = self._column_mapping(sdf, NASAPOWER_COLUMN_MAPPINGS)

        sdf = sdf.withColumn(
            "date",
            date_format(
                to_date(
                    col("date").cast("string"), "yyyyMMdd"), 
                    "yyyy-MM-dd"
                )
        ).withColumn(
            "city",
            lit(str(city))
        ).withColumn(
            "year",
            year(col("date"))
        )

        return sdf
    
    def openmeteo_data_processor(self):
        city_pbar = tqdm(self.config["cities"])
        for city in city_pbar:
            city_pbar.set_description(f"Processing {city}'s data")
            year_pbar = tqdm(
                range(
                    self.config["start_year"], 
                    self.config["end_year"] + 1
                ),
                leave= False
            )

            for year in year_pbar:
                year_pbar.set_description(f"Processing {city}'s {year} data")
                data_path = Path(self.config["openmeteo_bronze_storage_base_path"]) / city / str(year) / f"{city}_{year}.json"

                with open(data_path, "r") as file:
                    json_data = json.load(file)
                
                sdf = self._openmeteo_transformations(json_data, city)

                write_path = Path(self.config["openmeteo_silver_storage_base_path"]) / city / str(year)
                sdf.write.mode("overwrite").parquet(str(write_path))
    
    def nasapower_data_processor(self):
        city_pbar = tqdm(self.config["cities"])
        for city in city_pbar:
            city_pbar.set_description(f"Processing {city}'s data")
            year_pbar = tqdm(
                range(
                    self.config["start_year"], 
                    self.config["end_year"] + 1),
                    leave= False
                )
            for year in year_pbar:
                year_pbar.set_description(f"Processing {city}'s {year} data")
                data_path = Path(self.config["nasapower_bronze_storage_base_path"]) / city / str(year) / f"{city}_{year}.json"

                with open(data_path, "r") as file:
                    json_data = json.load(file)
                
                sdf = self._nasapower_transformations(json_data, city, NASAPOWER_SCHEMA)

                write_path = Path(self.config["nasapower_silver_storage_base_path"]) / city / str(year)
                sdf.write.mode("overwrite").parquet(str(write_path))

if __name__ == "__main__":
    process = WeatherDataProcessor()
    process.openmeteo_data_processor()
    process.nasapower_data_processor()