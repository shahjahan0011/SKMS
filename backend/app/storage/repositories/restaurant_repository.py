"""Fetch restaurant data from the database."""
from typing import List, Dict
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class restaurant_repository:
    """Repository for fetching restaurant data."""
    def __init__(self):
        self.file_path = "backend/app/storage/data/restaurants.csv"

    def get_all_restaurants(self) -> List[Dict]:
        """Fetch all restaurant data from the CSV file."""
        return CSVStore.read_csv(self.file_path)

    def get_restaurant_by_id(self, restaurant_id: str) -> Dict:
        """Fetch a restaurant by its ID from the CSV file."""
        all_restaurants = self.get_all_restaurants()

        for restaurant in all_restaurants:
            if str(restaurant.get("id")) == str(restaurant_id):
                return restaurant

        return None
