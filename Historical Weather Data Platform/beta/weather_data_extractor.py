import json
from pathlib import Path
from time import sleep
from typing import Any, TypedDict, cast
import requests
import yaml
from tqdm import tqdm
from WDataTypes import CityCoordinate, WeatherConfig

class WeatherDataExtractor:
    def __init__(self) -> None:
        with open("./config.yaml", "r", encoding="utf-8") as file:
            self.config: WeatherConfig = cast(WeatherConfig, yaml.safe_load(file))

        with open(self.config["coordinates_data_location"], "r", encoding="utf-8") as file:
            self.cities_coordinates: list[CityCoordinate] = cast(list[CityCoordinate], json.load(file))
    
    def _request_city_data(self, city):
        response = requests.get(f"{self.config["city_data_url"]}{city}")

        json_response = cast(dict[str, Any], json.loads(response.text))
        results = cast(list[dict[str, Any]], json_response["results"])
        first_result = results[0]

        selected: CityCoordinate = {
            "name": cast(str, first_result["name"]),
            "latitude": float(first_result["latitude"]),
            "longitude": float(first_result["longitude"]),
            "elevation": float(first_result["elevation"]),
        }

        return selected
    
    def city_info_collector(self, cities: list[str]) -> list[CityCoordinate]:
        """
            Gets the city names as input, returns a list of dictionaries with it's Latitude, Longitude co-ordinates
            and Elevation above sea level for each city given.
        """
        cities_coll: list[CityCoordinate] = []

        for city in cities:
            try:
                selected: CityCoordinate = self._request_city_data(city)

                cities_coll.append(selected)
                sleep(1)
            except:
                sleep(1)
                continue

        return cities_coll
    
    def _get_city_data(self, city):
        if city not in [city_data["name"] for city_data in self.cities_coordinates]:
            city_data = self.city_info_collector([city])[0]
            self.cities_coordinates.append(city_data)
            return city_data
        else:
            city_data = next(
                city_data for city_data in self.cities_coordinates
                if city_data["name"] == city
            )
            return city_data
    
    def _get_openmeteo_params(self, city_data, year):
        return {
            "latitude": city_data["latitude"],
            "longitude": city_data["longitude"],
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": self.config.get("openmeteo_daily", []),
            "timezone": self.config["timezone"],
        }
    
    def _get_meteostat_params(self, city_data, year):
        return {
            "lat": str(city_data["latitude"]),
            "lon": str(city_data["longitude"]),
            "alt": str(city_data["elevation"]),
            "start": f"{year}-01-01",
            "end": f"{year}-12-31"
        }
    
    def _get_nasapower_params(self, city_data, year):
        return {
            "parameters": ",".join(self.config["nasapower_daily"]),
            "community": "AG",
            "longitude": city_data["longitude"],
            "latitude": city_data["latitude"],
            "start": f"{year}0101",
            "end": f"{year}1231",
            "format": "JSON"
        }
    
    def _get_meteostat_headers(self):
        return {
            "x-rapidapi-key": self.config["meteostat_x-rapidapi-key"],
            "x-rapidapi-host": self.config["meteostat_x-rapidapi-host"],
            "Content-Type": "application/json"
        }
    
    def _select_parameters(self, api_id, city_data, year):
        if api_id == "openmeteo":
            return self._get_openmeteo_params(city_data, year)
        if api_id == "meteostat":
            return self._get_meteostat_params(city_data, year)
        if api_id == "nasapower":
            return self._get_nasapower_params(city_data, year)
        
        raise ValueError("Invalid API key")
    
    def _generate_file_path(self, base_path, city, year):
        year_path = base_path / city / str(year)
        year_path.mkdir(
            parents = True,
            exist_ok = True
        )

        return year_path / f"{city}_{year}.json"
    
    def _request_weather_data(self, url, params, api_id):
        for attempt in range(5):
            try:
                if api_id == "openmeteo":
                    response = requests.get(
                        url,
                        params=params,
                        timeout=30
                    )
                elif api_id == "meteostat":
                    response = requests.get(
                        url,
                        headers=self._get_meteostat_headers(),
                        params=params,
                        timeout=30
                    )
                elif api_id == "nasapower":
                    response = requests.get(
                        url,
                        params=params,
                        timeout=30
                    )
                else:
                    raise ValueError("Invalid API key")

                response.raise_for_status()

                data = response.json()

                if "daily" not in data:
                    raise ValueError(
                        f"Missing daily key."
                    )

                return data

            except Exception as exc:
                print(
                    f"Attempt {attempt + 1}/5 failed"
                )

                if attempt < 4:
                    sleep(2 ** attempt)
                    continue

                print(
                    f"Failed after 5 attempts."
                )

                return None
        
    def _write_data(self, file_path, data):
        with file_path.open("w") as file:
                json.dump(data, file, indent=4)
        
        return None
    
    def _dump_coordinate_data(self):
        with open(self.config["coordinates_data_location"], "w") as file:
            json.dump(self.cities_coordinates, file, indent=4)
    
    def _openmeteo_validation(self, file_path):
        if file_path.exists():
            try:
                with file_path.open(
                    "r",
                    encoding="utf-8"
                ) as file:
                    json_data = json.load(file)

                if "daily" in json_data:
                    return True

            except Exception:
                return False
    
    def _weather_data_collection_engine(self, api_id, url, base_path) -> None:
        city_pbar = tqdm(self.config["cities"])
        for city in city_pbar:
            city_pbar.set_description(f"Getting weather data of {city}")
            city_data = self._get_city_data(city)
            
            year_pbar = tqdm(
                    range(
                        self.config["start_year"],
                        self.config["end_year"] + 1
                    ),
                    leave = False
                )
            for year in year_pbar:
                year_pbar.set_description(
                    f"Getting data of {year}"
                )

                file_path = self._generate_file_path(
                    base_path,
                    city,
                    year
                )

                # Skip if a valid file already exists
                if file_path.exists():
                    try:
                        with file_path.open(
                            "r",
                            encoding="utf-8"
                        ) as file:
                            json_data = json.load(file)

                        if "daily" in json_data:
                            continue

                    except Exception:
                        pass

                params = self._select_parameters(
                    api_id,
                    city_data,
                    year
                )

                data = self._request_weather_data(
                    url,
                    params,
                    api_id
                )

                if data is None:
                    continue

                self._write_data(
                    file_path,
                    data
                )

                sleep(2)
        
        self._dump_coordinate_data()
    
    def openmeteo_weather_data_collector(self) -> None:
        url: str = self.config["openmeteo_url"]
        base_path = Path(self.config["openmeteo_bronze_storage_base_path"])
        api_id = "openmeteo"

        self._weather_data_collection_engine(api_id, url, base_path)
    
    def meteostat_weather_data_collector(self) -> None:
        url: str = self.config["meteostat_url"]
        base_path = Path(self.config["meteostat_bronze_storage_base_path"])
        api_id = "meteostat"

        self._weather_data_collection_engine(api_id, url, base_path)
    
    def nasapower_weather_data_collector(self) -> None:
        url: str = self.config["nasapower_url"]
        base_path = Path(self.config["nasapower_bronze_storage_base_path"])
        api_id = "nasapower"

        self._weather_data_collection_engine(api_id, url, base_path)


if __name__ == "__main__":
    weather = WeatherDataExtractor()
    print("Extracting data from Open Meteo")
    weather.openmeteo_weather_data_collector()
    # print("Extracting data from Nasa Power")
    # weather.nasapower_weather_data_collector()