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

