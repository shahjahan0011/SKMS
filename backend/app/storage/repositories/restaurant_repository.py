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
        restaurants = CSVStore.read_csv(self.file_path)

        for restaurant in restaurants:
            if not restaurant.get("id") or not restaurant.get("name"):
                raise ValueError("Invalid restaurant data")

        return restaurants

    def get_restaurant_by_id(self, restaurant_id: str):
        """Get a restaurant by restaurant id"""
        restaurants = CSVStore.read_csv(self.file_path)

        for restaurant in restaurants:
            if restaurant["id"] == restaurant_id:
                return restaurant

        return None
