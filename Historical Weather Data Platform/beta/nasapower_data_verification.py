import json
from pathlib import Path
from typing import cast

import yaml
from tqdm import tqdm

from WDataTypes import WeatherConfig


class NasaPowerDataVerifier:
    def __init__(self) -> None:
        with open("./config.yaml", "r", encoding="utf-8") as file:
            self.config: WeatherConfig = cast(
                WeatherConfig,
                yaml.safe_load(file)
            )

    def verify_files(self) -> None:
        invalid_files: list[str] = []

        required_keys = {
            "type",
            "geometry",
            "properties",
            "header",
            "messages",
            "parameters",
            "times"
        }

        city_pbar = tqdm(
            self.config["cities"],
            desc="Verifying cities"
        )

        for city in city_pbar:
            for year in range(
                self.config["start_year"],
                self.config["end_year"] + 1
            ):
                file_path = (
                    Path(
                        self.config[
                            "nasapower_bronze_storage_base_path"
                        ]
                    )
                    / city
                    / str(year)
                    / f"{city}_{year}.json"
                )

                try:
                    with file_path.open(
                        "r",
                        encoding="utf-8"
                    ) as file:
                        json_data = json.load(file)

                    missing_keys = (
                        required_keys - set(json_data.keys())
                    )

                    if missing_keys:
                        raise KeyError(
                            f"Missing keys: {missing_keys}"
                        )

                except Exception:
                    invalid_files.append(str(file_path))

        print("\nVerification Summary")
        print("-" * 30)
        print(
            f"Total Files Checked : "
            f"{len(self.config['cities']) * (self.config['end_year'] - self.config['start_year'] + 1)}"
        )
        print(
            f"Invalid Files       : "
            f"{len(invalid_files)}"
        )

        if invalid_files:
            print("\nInvalid Files:")
            for file in invalid_files:
                print(file)
        else:
            print("\nAll files are valid.")


if __name__ == "__main__":
    verifier = NasaPowerDataVerifier()
    verifier.verify_files()