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
        """Fetch all menu data from the CSV file and convert type for M4."""

        raw_menus = CSVStore.read_csv(self.file_path)
        formatted_menus = []

        for item in raw_menus:
            item["id"] = int(item["id"])
            item["restaurant_id"] = int(item["restaurant_id"])
            item["price"] = float(item["price"])

            item["stock_count"] = int(item.get("stock_count", 0))
            item["is_available"] = str(item.get("is_available", "")).strip().lower() == "true"

            formatted_menus.append(item)

        return formatted_menus

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
                if any(q in str(value).lower() for value in item.values())
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

    def get_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Fetch menu items for a specific restaurant."""
        all_menus = self.get_all()
        return [
            item for item in all_menus
            if str(item.get("restaurant_id")) == str(restaurant_id)
        ]

    def get_menu_item_by_id(self, item_id: str) -> Optional[dict]:
        """Fetch a menu item by its ID."""
        all_menus = self.get_all()
        for item in all_menus:
            if str(item.get("id")) == str(item_id):
                return item
        return None

    def get_menu_by_filters(
        self,
        restaurant_id: Optional[str] = None,
        item_name: Optional[str] = None,
        price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Fetch menu items with optional global filters."""
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

        if price is not None:
            filtered_menus = [
                item for item in filtered_menus
                if float(item.get("price", 0)) <= price
            ]

        return filtered_menus


# New M4 inventory methods
    def update_item_inventory(self, item_id: str, new_stock: int, is_available: bool) -> bool:
        """
        M4 Admin Feature: Updates the stock count and availability
        of a specific menu item and saves it back to the CSV.
        """
        items = []
        updated = False

        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            items = list(reader)

        for item in items:
            if str(item.get("id")) == str(item_id):
                item["stock_count"] = str(new_stock)
                item["is_available"] = str(is_available)
                updated = True
                break

        if updated:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["id", "restaurant_id", "item_name", "price", "stock_count", "is_available"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(items)

        return updated


    def deduct_inventory(self, item_id: str, quantity_ordered: int) -> Dict[str, Any]:
        """
        M4 Deducts stock safely and automatically toggles availability.
        """

        items = []
        item_found = False

        result = {
            "success": False,
            "error": None,
            "new_stock": 0,
            "sold_out_just_now": False,
            "low_stock_warning": False
        }

        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            items = list(reader)

        for item in items:
            if str(item.get("id")) == str(item_id):
                item_found = True
                current_stock = int(item.get("stock_count", 0))

                # Prevent negative stock
                if current_stock < quantity_ordered:
                    result["error"] = f"Insufficient stock. Only {current_stock} left."
                    return result

                #Calculate new stock
                new_stock = current_stock - quantity_ordered
                item["stock_count"] = str(new_stock)

                # Auto-toggle availability if it hits exactly 0
                if new_stock == 0:
                    item["is_available"] = "False"
                    result["sold_out_just_now"] = True
                else:
                    item["is_available"] = "True"

                # Trigger a low stock warning for the Admin
                if 0 < new_stock <= 5:
                    result["low_stock_warning"] = True

                result["success"] = True
                result["new_stock"] = new_stock
                break

        if not item_found:
            result["error"] = "Item not found in database."
            return result

        # Only save to the CSV if the deduction was successful
        if result["success"]:
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ["id", "restaurant_id", "item_name", "price", "stock_count", "is_available"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(items)

        return result


