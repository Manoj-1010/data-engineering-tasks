from typing import Any, TypedDict

CityCoordinate = TypedDict(
    "CityCoordinate",
    {
        "name": str,
        "latitude": float,
        "longitude": float,
        "elevation": float,
    },
)

WeatherConfig = TypedDict(
    "WeatherConfig",
    {
        "cities": list[str],
        "openmeteo_url": str,
        "meteostat_url": str,
        "nasapower_url": str,
        "timezone": str,
        "start_year": int,
        "end_year": int,
        "openmeteo_bronze_storage_base_path": str,
        "meteostat_bronze_storage_base_path": str,
        "nasapower_bronze_storage_base_path": str,
        "silver_storage_base_path": str,
        "coordinates_data_location": str,
        "openmeteo_daily": list[str],
        "meteostat_x-rapidapi-key": str,
        "meteostat_x-rapidapi-host": str,
        "nasapower_daily": list[str],
        "city_data_url": str
    },
)