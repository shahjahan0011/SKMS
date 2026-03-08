"""Menu repository for fetching menu data."""
from typing import List, Dict
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class MenuRepository:
    """Repository for fetching menu data."""
    def __init__(self):
        self.file_path = "backend/app/storage/data/menus.csv"

    def get_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Fetch menu items for a specific restaurant from the CSV file."""
        all_menus = CSVStore.read_csv(self.file_path)

        for menu in all_menus:
            if not menu.get("id") or not menu.get("restaurant_id") or not menu.get("price"):
                raise ValueError("Invalid menu data")
        
        return [
            menu for menu in all_menus
            if menu['restaurant_id'] == restaurant_id
            ]

    def get_menu_item_by_id(self, item_id: str):
        """Get menu item by id"""
        menus = CSVStore.read_csv(self.file_path)

        for item in menus:
            if item["id"] == item_id:
                return item

        return None