
import csv

from collectors.base_collector import BaseCollector


class CSVCollector(BaseCollector):
    """Collect listing records from a CSV file."""

    def collect(self):

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.file_path}"
            )

        with open(
            self.file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            valid_lines = (
                line for line in file if line.strip()
            )

            reader = csv.DictReader(valid_lines)

            if not reader.fieldnames:
                raise ValueError(
                    "CSV file has no headers."
                )

            records = list(reader)

        if not records:
            raise ValueError(
                "CSV file contains no listings."
            )

        return records
