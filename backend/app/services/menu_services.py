"""Menu services module."""

from typing import Optional, List, Dict, Any
from app.storage.repositories.menu_repository import menu_repository
from app.storage.repositories.restaurant_repository import restaurant_repository

# pylint: disable=too-few-public-methods
class MenuService:
    """Service class for menu-related operations."""

    def __init__(self, menu_repo: menu_repository, res_repo: restaurant_repository):
        self.menu_repo = menu_repo
        self.restaurant_repo = res_repo

    def get_all_menus_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get all menus for a specific restaurant."""
        return self.menu_repo.get_menu_by_restaurant(restaurant_id)

    def get_active_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get active menu items for a specific restaurant."""
        all_menus = self.menu_repo.get_menu_by_restaurant(restaurant_id)
        # Handles various ways 'active' might be stored
        active_menus = [
            menu for menu in all_menus 
            if str(menu.get('is_available', menu.get('status', ''))).lower() in ['true', '1', 'yes']
        ]
        return active_menus

    def get_active_menu_paginated_by_restaurant(
        self,
        restaurant_id: str,
        search_query: Optional[str],
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """Bridge between router and repository for paginated menus."""

        return self.menu_repo.get_active_menu_paginated_by_restaurant(
            restaurant_id=restaurant_id,
            search_query=search_query,
            page=page,
            page_size=page_size
        )

    def get_menu_item_by_id(self, item_id: str) -> Dict:
        """Get menu item by id."""
        return self.menu_repo.get_menu_item_by_id(item_id)

    def get_global_menus(
        self,
        restaurant_id: Optional[str] = None,
        item_name: Optional[str] = None,
        price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search globally then apply filters and attach restaurant names."""
        items = self.menu_repo.get_menu_by_filters(
            restaurant_id=restaurant_id,
            item_name=item_name,
            price=price
        )

        active_items = [item for item in items if str(item.get('is_available', '')).lower() == 'true']

        all_restaurants = self.restaurant_repo.get_all()
        restaurants = {res['id']: res['name'] for res in all_restaurants}

        for item in active_items:
            res_id = item.get('restaurant_id')
            item["restaurant_name"] = restaurants.get(res_id, "Unknown Kitchen")
   
            if "description" not in item:
                item["description"] = "No description available"

        return active_items
      

    def browse_menu(self, restaurant_id: str, search_query: Optional[str] = None, page: int = 1, page_size: int = 10):
        """Wrapper to match the 'browse' naming convention."""
        return self.get_active_menu_paginated_by_restaurant(
            restaurant_id=restaurant_id,
            search_query=search_query,
            page=page,
            page_size=page_size
        )
