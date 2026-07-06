from __future__ import annotations

from typing import Any

from WDataTypes import CityCoordinate


def build_city_lookup_params(
    city: str,
) -> dict[str, str]:
    """
    Build query parameters for the city geocoding API.

    Parameters
    ----------
    city : str
        City name.

    Returns
    -------
    dict[str, str]
        Query parameters.
    """

    return {
        "name": city,
        "count": "1",
    }


def build_openmeteo_params(
    city: CityCoordinate,
    year: int,
    daily_variables: list[str],
    timezone: str,
) -> dict[str, Any]:
    """
    Build request parameters for the Open-Meteo Archive API.

    Parameters
    ----------
    city : CityCoordinate
        City metadata.

    year : int
        Target year.

    daily_variables : list[str]
        Daily weather variables.

    timezone : str
        Timezone for returned timestamps.

    Returns
    -------
    dict[str, Any]
    """

    return {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": f"{year}-01-01",
        "end_date": f"{year}-12-31",
        "daily": ",".join(daily_variables),
        "timezone": timezone,
    }


def build_nasapower_params(
    city: CityCoordinate,
    year: int,
    parameters: list[str],
) -> dict[str, Any]:
    """
    Build request parameters for the NASA POWER API.

    Parameters
    ----------
    city : CityCoordinate
        City metadata.

    year : int
        Target year.

    parameters : list[str]
        NASA POWER weather parameters.

    Returns
    -------
    dict[str, Any]
    """

    return {
        "parameters": ",".join(parameters),
        "community": "AG",
        "longitude": city["longitude"],
        "latitude": city["latitude"],
        "start": f"{year}0101",
        "end": f"{year}1231",
        "format": "JSON",
    }