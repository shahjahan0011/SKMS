"""Menu services module."""

from typing import Any, Dict, List, Optional
from app.storage.repositories.menu_repository import MenuRepository
from app.storage.repositories.restaurant_repository import RestaurantRepository

# pylint: disable=too-few-public-methods
class MenuService:
    """Service class for menu-related operations."""
    def __init__(self, menu_repo, restaurant_repo):
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    def get_all_menus_by_restaurant(
        self,
        restaurant_id: str,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> List[Dict]:
        """Get all menu items for a specific restaurant."""
        return self.menu_repo.get_menu_by_restaurant(restaurant_id)

    def get_active_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get active menu items for a specific restaurant."""
        all_menus = self.menu_repo.get_menu_by_restaurant(restaurant_id)

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
        return self.menu_repo.get_menu_item_by_id(item_id)

    def get_global_menus(
            self,
            restaurant_id: Optional[str] = None,
            item_name: Optional[str] = None,
            price: Optional[float] = None
            ) -> List[Dict[str, Any]]:

        # Inside get_global_menus
        all_res = self.restaurant_repo.get_all()
        print(f"DEBUG: First restaurant data: {all_res[0] if all_res else 'Empty'}")


        """Search for menu globally then apply filter for restauratanst and price."""
        items = self.menu_repo.get_menu_by_filters(
            restaurant_id,
            item_name,
            price)

        active_items = [item for item in items if str(item.get('is_available', '')).lower() == 'true']

        restaurants = {res['id']: res['name'] for res in self.restaurant_repo.get_all()}

        for item in active_items:
            res_id = item.get('restaurant_id')
            item["restaurant_name"] = restaurants.get(res_id, "Unknown Kitchen")

        return active_items


