"""
Column mappings for converting source-specific weather data
into the project's canonical weather schema.
"""

OPENMETEO_COLUMN_MAPPINGS = {
    # Temperature
    "temperature_2m_mean": "temperature_mean",
    "temperature_2m_max": "temperature_max",
    "temperature_2m_min": "temperature_min",
    "apparent_temperature_mean": "apparent_temperature",

    # Precipitation
    "precipitation_sum": "precipitation",
    "rain_sum": "rain_sum",
    "snowfall_sum": "snowfall_sum",
    "precipitation_hours": "precipitation_hours",

    # Atmospheric
    "relative_humidity_2m_mean": "relative_humidity",
    "pressure_msl_mean": "pressure_msl",

    # Wind
    "wind_speed_10m_mean": "wind_speed_mean",
    "wind_speed_10m_max": "wind_speed_max",
    "wind_gusts_10m_max": "wind_gusts_max",
    "wind_direction_10m_dominant": "wind_direction",

    # Clouds
    "cloud_cover_mean": "cloud_cover",

    # Radiation
    "shortwave_radiation_sum": "shortwave_radiation",

    # Time
    "time": "date",
}


NASAPOWER_COLUMN_MAPPINGS = {
    # Temperature
    "T2M": "temperature_mean",
    "T2M_MAX": "temperature_max",
    "T2M_MIN": "temperature_min",
    "TS": "surface_temperature",
    "T2MDEW": "dew_point_temperature",

    # Precipitation
    "PRECTOTCORR": "precipitation",

    # Radiation
    "ALLSKY_SFC_SW_DWN": "shortwave_radiation",

    # Humidity
    "RH2M": "relative_humidity",

    # Pressure
    "PS": "surface_pressure",

    # Clouds
    "CLOUD_AMT": "cloud_cover",
}