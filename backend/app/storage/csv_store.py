"""CVSStore: A simple class to handle reading CSV files and returning their contents as a list of dictionaries.
This class provides a static method `read_csv` that takes a file path as input and returns a list of dictionaries, 
where each dictionary represents a row in the CSV file, with the keys being the column headers and the values being the corresponding cell values.
 
"""
import csv
from typing import List, Dict

class CSVStore:
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, str]]:
        """Reads a CSV file and returns a list of dictionaries."""
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                return [row for row in reader]
            
        #If the file is not found, it prints an error message and returns an empty list.
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
            return []
        