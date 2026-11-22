import json

from collectors.base_collector import BaseCollector


class JSONCollector(BaseCollector):
    """Collect listing records from a JSON file."""

    def collect(self):

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"JSON file not found: {self.file_path}"
            )

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "JSON file must contain a list of listings."
            )

        for index, record in enumerate(data):
            if not isinstance(record, dict):
                raise ValueError(
                    f"Invalid listing at index {index}."
                )

        return data
