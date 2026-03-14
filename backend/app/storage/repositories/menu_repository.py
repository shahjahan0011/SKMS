"""Menu repository for fetching menu data."""
import csv
from typing import List, Dict, Optional
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
    
    def get_menu_item_by_id(self, id: str) -> Optional[dict]:
        with open(self.file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_id = row.get("id")
                if row_id == id:
                    return row
        return None