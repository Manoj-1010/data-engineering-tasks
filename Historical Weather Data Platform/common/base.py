from abc import ABC

from common.config_loader import load_config
from WDataTypes import WeatherConfig


class BasePipeline(ABC):
    """
    Base class for all pipeline components.

    Provides access to the project configuration.
    """

    def __init__(self, config_path: str = "./config.yaml") -> None:
        self.config: WeatherConfig = load_config(config_path)