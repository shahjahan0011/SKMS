"""Menu repository for fetching menu data."""
from typing import Any, List, Dict, Optional
import os
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class menu_repository:
    """Repository for fetching menu data."""
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "data", "menus.csv")
        self.file_path = os.path.abspath(self.file_path)
        # app/storage/repositories/../data/menus.csv


    def get_all(self) -> List[Dict]:
        """Fetch all menu data from the CSV file."""
        return CSVStore.read_csv(self.file_path)


    def get_menu_by_restaurant(
            self,
            restaurant_id: str,
            search: Optional[str] = None,
            page: int = 1,
            page_size: int = 10
            ) -> List[Dict]:
        """Fetch menu items for a specific restaurant from the CSV file."""
        all_menus = self.get_all()

        filtered_menus = [
            item for item in all_menus
            if str(item.get("restaurant_id")) == str(restaurant_id)
        ]

        if search:
            search_lower = search.lower()
            filtered_menus = [
                item for item in filtered_menus
                if search_lower in str(item.get("item_name", "")).lower()
            ]

        start = (page - 1) * page_size
        end = start + page_size

        return filtered_menus[start:end]


    def get_menu_item_by_id(self, menu_item_id: str):
        """Fetch a menu item by its ID from the CSV file."""
        all_menus = self.get_all()

        for item in all_menus:
            if str(item.get("id")) == str(menu_item_id):
                return item
        return None


    def get_menu_by_filters(
        self,
        restaurant_id: Optional[str] = None,
        item_name: Optional[str] = None,
        price: Optional[float] = None
        ) -> List[Dict[str, Any]]:

        """Fetch menu items for a specific restaurant with optional search query."""
        filtered_menus = self.get_all()

        if restaurant_id:
            filtered_menus = [
                item for item in filtered_menus
                if str(item.get("restaurant_id")) == str(restaurant_id)
            ]

        if item_name:
            item_name_lower = item_name.lower()
            filtered_menus = [
                item for item in filtered_menus
                if item_name_lower in str(item.get("item_name", "")).lower()
            ]
            return filtered_menus

        if price is not None:
            filtered_menus = [
                item for item in filtered_menus
                if float(item.get("price", 0)) <= price
            ]
            return filtered_menus

        return filtered_menus
