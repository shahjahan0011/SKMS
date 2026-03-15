"""Menu repository for fetching menu data."""
from typing import Any, List, Dict, Optional
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class MenuRepository:
    """Repository for fetching menu data."""
    def __init__(self):
        self.file_path = "app/storage/data/menus.csv"


    def get_all(self) -> List[Dict]:
        """Fetch all menu data from the CSV file."""
        return CSVStore.read_csv(self.file_path)


    def get_active_menu_paginated_by_restaurant(
        self,
        restaurant_id: str,
        search_query: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Fetch paginated menu items and return total count for metadata."""
        all_menus = self.get_all()

        filtered_menus = [
            item for item in all_menus
            if str(item.get("restaurant_id")) == str(restaurant_id)
        ]

        if search_query:
            q = search_query.lower()
            filtered_menus = [
                item for item in filtered_menus
                if q in str(item.get("item_name", "")).lower()
            ]

        total_count = len(filtered_menus)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_items = filtered_menus[start:end]

        return {
            "items": paginated_items,
            "total": total_count,
            "page": page,
            "page_size": page_size
        }


    def get_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Legacy method for other parts of the app."""
        result = self.get_active_menu_paginated_by_restaurant(restaurant_id)
        return result.get("items", [])


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
