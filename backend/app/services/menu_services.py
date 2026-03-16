"""Menu services module."""

from typing import Any
from app.storage.repositories.menu_repository import menu_repository

# pylint: disable=too-few-public-methods
class MenuService:
    """Service class for menu-related operations."""
    def __init__(self, repo: menu_repository):
        self.menu_repository = repo

    def get_all_menus_by_restaurant(self, restaurant_id: str) -> list[dict]:
        """Get all menu items for a specific restaurant."""
        return self.menu_repository.get_menu_by_restaurant(restaurant_id)

    def get_active_menu_by_restaurant(self, restaurant_id: str) -> list[dict]:
        """Get active menu items for a specific restaurant."""
        all_menus = self.menu_repository.get_menu_by_restaurant(restaurant_id)

        active_menus = [
            menu for menu in all_menus
            if str(menu.get('is_available', '')).strip().lower() in ('true', '1', 'yes')
        ]
        return active_menus

    def get_paginated_menu_by_restaurant(self, restaurant_id: str, page: int, page_size: int, search: str = "") -> dict[str, Any]:
        """Get paginated menu items for a specific restaurant."""
        active_menus = self.get_active_menu_by_restaurant(restaurant_id)

        if search:
            search_lower = search.lower()
            active_menus = [
                menu for menu in active_menus
                if search_lower in menu.get("name", "").lower()
                or search_lower in menu.get("description", "").lower()
            ]

        total_items = len(active_menus)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_items = active_menus[start_index:end_index]

        return {
            "items": paginated_items,
            "total_items": total_items,
            "page": page,
            "page_size": page_size,
            "total_pages": (total_items + page_size - 1) // page_size
        }

    def get_menu_item_by_id(self, item_id: str) -> dict:
        """Get menu item by id."""
        return self.menu_repository.get_menu_item_by_id(item_id)
