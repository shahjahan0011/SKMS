"""CVSStore:
"""
import csv
from typing import List, Dict

#A simple class to handle reading CSV files and returning their contents
#pylint: disable=too-few-public-methods
class CSVStore:
    """A utility class to handle reading from CSV files."""

    @staticmethod
    def read_csv(file_path: str) -> List[Dict]:
        """Reads a CSV file and returns a list of dictionaries."""
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                return list(reader)

        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return []
