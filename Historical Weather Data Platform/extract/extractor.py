from __future__ import annotations

import json
from pathlib import Path
from time import sleep
from typing import Any

import requests
from tqdm import tqdm

from common.base import BasePipeline
from common.writer import write_json

from extract.api_clients import (
    OpenMeteoClient,
    NASAPowerClient,
)

from extract.params import (
    build_city_lookup_params,
    build_openmeteo_params,
    build_nasapower_params,
)

from WDataTypes import CityCoordinate


class WeatherDataExtractor(BasePipeline):
    """
    Extract historical weather data from public APIs and store
    the raw responses in the Bronze layer.
    """

    def __init__(self) -> None:
        super().__init__()

        self.openmeteo_client = OpenMeteoClient(
            self.config["openmeteo_url"]
        )

        self.nasa_client = NASAPowerClient(
            self.config["nasapower_url"]
        )

        self.coordinate_file = Path(
            self.config["coordinates_data_location"]
        )

        self.cities_coordinates = self._load_coordinates()

    # ---------------------------------------------------------
    # Coordinate Management
    # ---------------------------------------------------------

    def _load_coordinates(self) -> list[CityCoordinate]:
        if not self.coordinate_file.exists():
            return []

        with self.coordinate_file.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def _save_coordinates(self) -> None:
        write_json(
            self.coordinate_file,
            self.cities_coordinates,
        )

    def _request_city_coordinates(
        self,
        city: str,
    ) -> CityCoordinate:

        response = requests.get(
            self.config["city_data_url"],
            params=build_city_lookup_params(city),
            timeout=30,
        )

        response.raise_for_status()

        result = response.json()["results"][0]

        return {
            "name": result["name"],
            "latitude": float(result["latitude"]),
            "longitude": float(result["longitude"]),
            "elevation": float(result["elevation"]),
        }

    def _get_city_coordinates(
        self,
        city: str,
    ) -> CityCoordinate:

        for record in self.cities_coordinates:
            if record["name"] == city:
                return record

        coordinates = self._request_city_coordinates(city)

        self.cities_coordinates.append(coordinates)

        return coordinates

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    @staticmethod
    def _is_valid_openmeteo(data: dict[str, Any]) -> bool:
        return "daily" in data

    @staticmethod
    def _is_valid_nasa(data: dict[str, Any]) -> bool:
        return (
            "properties" in data
            and "parameter" in data["properties"]
        )

    # ---------------------------------------------------------
    # Storage
    # ---------------------------------------------------------

    def _bronze_file_path(
        self,
        base_path: str,
        city: str,
        year: int,
    ) -> Path:

        return (
            Path(base_path)
            / city
            / str(year)
            / f"{city}_{year}.json"
        )

    # ---------------------------------------------------------
    # Extraction Engine
    # ---------------------------------------------------------

    def _collect_openmeteo(
        self,
        city_data: CityCoordinate,
        city: str,
        year: int,
    ) -> None:

        output = self._bronze_file_path(
            self.config["openmeteo_bronze_storage_base_path"],
            city,
            year,
        )

        if output.exists():
            return

        params = build_openmeteo_params(
            city_data,
            year,
            self.config["openmeteo_daily"],
            self.config["timezone"],
        )

        data = self.openmeteo_client.fetch(params)

        if not self._is_valid_openmeteo(data):
            return

        write_json(output, data)

    def _collect_nasa(
        self,
        city_data: CityCoordinate,
        city: str,
        year: int,
    ) -> None:

        output = self._bronze_file_path(
            self.config["nasapower_bronze_storage_base_path"],
            city,
            year,
        )

        if output.exists():
            return

        params = build_nasapower_params(
            city_data,
            year,
            self.config["nasapower_daily"],
        )

        data = self.nasa_client.fetch(params)

        if not self._is_valid_nasa(data):
            return

        write_json(output, data)

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def collect(self) -> None:

        city_progress = tqdm(
            self.config["cities"],
            desc="Cities",
        )

        for city in city_progress:

            city_data = self._get_city_coordinates(city)

            year_progress = tqdm(
                range(
                    self.config["start_year"],
                    self.config["end_year"] + 1,
                ),
                leave=False,
                desc=city,
            )

            for year in year_progress:

                self._collect_openmeteo(
                    city_data,
                    city,
                    year,
                )

                self._collect_nasa(
                    city_data,
                    city,
                    year,
                )

                sleep(2)

        self._save_coordinates()


if __name__ == "__main__":

    WeatherDataExtractor().collect()