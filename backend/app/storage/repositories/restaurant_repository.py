"""Fetch restaurant data from the database."""

from typing import List, Dict
from backend.app.storage.csv_store import CSVStore

class restaurant_repository:
    """Repository for fetching restaurant data."""

    def __init__(self):
        self.file_path = "app/storage/restaurants.csv"

    def get_all_restaurants(self) -> List[Dict[str, str]]:
        """Fetch all restaurant data from the CSV file."""
        return CSVStore.read_csv(self.file_path)    
