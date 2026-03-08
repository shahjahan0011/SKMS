"""Menu repository for fetching menu data."""
from typing import List, Dict
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class MenuRepository:
    """Repository for fetching menu data."""
    def __init__(self):
        self.file_path = "backend/app/storage/data/menus.csv"

    def get_all(self) -> List[Dict]:
        """Fetch all menu data from the CSV file."""
        return CSVStore.read_csv(self.file_path)

    def get_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Fetch menu items for a specific restaurant from the CSV file."""
        all_menus = self.get_all

        return [
            item for item in all_menus
            if str(item.get("id")) == str(restaurant_id)
            ]
