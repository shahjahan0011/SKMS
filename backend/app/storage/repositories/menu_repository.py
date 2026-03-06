"""Menu repository for fetching menu data."""
from typing import List, Dict
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class MenuRepository:
    """Repository for fetching menu data."""
    def __init__(self):
        self.file_path = "app/storage/data/menu_items.csv"

    def get_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Fetch menu items for a specific restaurant from the CSV file."""
        all_menus = CSVStore.read_csv(self.file_path)
        return [
            menu for menu in all_menus
            if menu['restaurant_id'] == restaurant_id
            ]
