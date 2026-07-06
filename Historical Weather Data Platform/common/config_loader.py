from typing import cast

import yaml

from WDataTypes import WeatherConfig


def load_config(config_path: str = "./config.yaml") -> WeatherConfig:
    """
    Load the project configuration.

    Parameters
    ----------
    config_path : str
        Path to config.yaml

    Returns
    -------
    WeatherConfig
    """

    with open(config_path, "r", encoding="utf-8") as file:
        return cast(
            WeatherConfig,
            yaml.safe_load(file)
        )