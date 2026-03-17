"""Menu repository for fetching menu data."""
import os
import csv
from typing import List, Dict, Optional, Any
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class menu_repository:
    """Repository for fetching menu data using snake_case."""
    
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "data", "menus.csv")
        self.file_path = os.path.abspath(self.file_path)

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

        total_pages = (total_count + page_size - 1) // page_size if page_size > 0 else 0

        return {
            "items": paginated_items,
            "total_items": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    def get_menu_by_restaurant(self, restaurant_id: str)