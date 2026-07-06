OPENMETEO_COLUMN_MAPPINGS = {
    "time": "date",
    "temperature_2m_mean": "temperature_mean",
    "temperature_2m_max": "temperature_max",
    "temperature_2m_min": "temperature_min",

    "apparent_temperature_mean": "apparent_temperature",

    "precipitation_sum": "precipitation",

    "relative_humidity_2m_mean": "relative_humidity",

    "wind_speed_10m_mean": "wind_speed_mean",
    "wind_speed_10m_max": "wind_speed_max",
    "wind_gusts_10m_max": "wind_gusts_max",
    "wind_direction_10m_dominant": "wind_direction",

    "cloud_cover_mean": "cloud_cover",

    "shortwave_radiation_sum": "shortwave_radiation",

    "pressure_msl_mean": "pressure_msl"
}

NASAPOWER_COLUMN_MAPPINGS = {
    # Temperature (aligned with Open-Meteo)
    "T2M": "temperature_mean",
    "T2M_MAX": "temperature_max",
    "T2M_MIN": "temperature_min",

    # Precipitation
    "PRECTOTCORR": "precipitation",

    # Solar Radiation
    "ALLSKY_SFC_SW_DWN": "shortwave_radiation",

    # Humidity
    "RH2M": "relative_humidity",
    "T2MDEW": "dew_point_temperature",

    # Pressure
    "PS": "surface_pressure",

    # Clouds
    "CLOUD_AMT": "cloud_cover",

    # Surface
    "TS": "surface_temperature"
}