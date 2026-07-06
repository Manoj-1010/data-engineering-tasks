from pyspark.sql.types import *

OPENMETEO_SCHEMA = StructType([
    StructField("time", StringType(), False),

    StructField("weather_code", DoubleType(), True),

    StructField("temperature_2m_mean", DoubleType(), True),
    StructField("temperature_2m_max", DoubleType(), True),
    StructField("temperature_2m_min", DoubleType(), True),
    StructField("apparent_temperature_mean", DoubleType(), True),

    StructField("precipitation_sum", DoubleType(), True),
    StructField("rain_sum", DoubleType(), True),
    StructField("snowfall_sum", DoubleType(), True),
    StructField("precipitation_hours", DoubleType(), True),

    StructField("relative_humidity_2m_mean", DoubleType(), True),

    StructField("wind_speed_10m_mean", DoubleType(), True),
    StructField("wind_speed_10m_max", DoubleType(), True),
    StructField("wind_gusts_10m_max", DoubleType(), True),
    StructField("wind_direction_10m_dominant", DoubleType(), True),

    StructField("cloud_cover_mean", DoubleType(), True),

    StructField("sunshine_duration", DoubleType(), True),
    StructField("shortwave_radiation_sum", DoubleType(), True),

    StructField("pressure_msl_mean", DoubleType(), True),

    StructField("sunrise", StringType(), True),
    StructField("sunset", StringType(), True),

    StructField("daylight_duration", DoubleType(), True)
])

NASAPOWER_SCHEMA = StructType([
    StructField("date", StringType(), False),

    StructField("T2M", DoubleType(), True),
    StructField("T2M_MAX", DoubleType(), True),
    StructField("T2M_MIN", DoubleType(), True),

    StructField("PRECTOTCORR", DoubleType(), True),

    StructField("ALLSKY_SFC_SW_DWN", DoubleType(), True),

    StructField("RH2M", DoubleType(), True),

    StructField("T2MDEW", DoubleType(), True),

    StructField("PS", DoubleType(), True),

    StructField("CLOUD_AMT", DoubleType(), True),

    StructField("TS", DoubleType(), True)
])