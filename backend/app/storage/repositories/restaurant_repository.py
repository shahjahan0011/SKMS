"""Fetch restaurant data from the database."""
import os
from typing import List, Dict
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class RestaurantRepository:
    """Repository for fetching restaurant data."""
    
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "data", "restaurants.csv")
        self.file_path = os.path.abspath(self.file_path)

        
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

      
    def get_restaurants_by_search(self, search_name: str = None):
        """ Search restaurants by name"""
        all_res = self.get_all()

        if search_name:
            query = search_name.lower()
            return [
                res for res in all_res
                if query in str(res.get("name", "")).lower()
                or query in str(res.get("cuisine", "")).lower()
            ]

        return all_res


    def get_all(self) -> List[Dict]:
        """Fetch all restaurant data from the CSV file."""
        return self.get_all_restaurants()
