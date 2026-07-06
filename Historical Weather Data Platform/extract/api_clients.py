from __future__ import annotations

from abc import ABC
from time import sleep
from typing import Any

import requests


class BaseApiClient(ABC):
    """
    Base HTTP client for weather APIs.

    Handles:
    - HTTP requests
    - Retry mechanism
    - Timeout
    - Status validation

    Child classes only need to provide:
    - url
    - headers (if required)
    """

    def __init__(
        self,
        url: str,
        timeout: int = 30,
        retries: int = 5,
    ) -> None:
        self.url = url
        self.timeout = timeout
        self.retries = retries

    @property
    def headers(self) -> dict[str, str] | None:
        """
        Override in child classes if the API requires headers.
        """
        return None

    def fetch(self, params: dict[str, Any]) -> dict[str, Any]:
        """
        Send a GET request and return the JSON response.

        Raises
        ------
        RuntimeError
            If all retry attempts fail.
        """

        last_exception: Exception | None = None

        for attempt in range(self.retries):
            try:
                response = requests.get(
                    self.url,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout,
                )

                response.raise_for_status()

                return response.json()

            except Exception as exc:
                last_exception = exc

                if attempt < self.retries - 1:
                    sleep(2**attempt)

        raise RuntimeError(
            f"Failed to fetch data from {self.url}"
        ) from last_exception


class OpenMeteoClient(BaseApiClient):
    """
    Client for the Open-Meteo Archive API.
    """

    pass

class NASAPowerClient(BaseApiClient):
    """
    Client for NASA POWER Daily API.
    """

    pass