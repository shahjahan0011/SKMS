"""Menu services module.""""

from typing import Any, Dict, List, Optional
from fastapi import HTTPException
from app.storage.repositories.menu_repository import MenuRepository
from app.storage.repositories.restaurant_repository import RestaurantRepository

# pylint: disable=too-few-public-methods
class MenuService:
    """Service class for menu-related operations."""

    def __init__(self, menu_repo: MenuRepository, restaurant_repo: RestaurantRepository):
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    def get_all_menus_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get all menus for a specific restaurant."""
        result = self.get_active_menu_paginated_by_restaurant(
            restaurant_id=restaurant_id,
            search_query=None,
            page=1,
            page_size=1000
        )
        return result.get("items", [])

    def get_active_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get active menu items for a specific restaurant."""
        all_menus = self.menu_repo.get_menu_by_restaurant(restaurant_id)
 
        active_menus = [
            menu for menu in all_menus 
            if str(menu.get('is_available', menu.get('status', ''))).lower() in ['true', '1', 'yes']
        ]
        return active_menus

    def get_menu_item_details(self, restaurant_id: str, item_id: str):
        """ Retrieve menu items details (FR6) """
        item = self.menu_repo.get_menu_item_by_id(restaurant_id, item_id)

        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        item["description"] = item.get("description", "No description available")
        raw_val = str(item.get("is_available", "False")).lower()
        item["is_available"] = raw_val == "true"

        return item

    def get_active_menu_paginated_by_restaurant(
        self,
        restaurant_id: str,
        search_query: str,
        page: int,
        page_size: int
    ):
        """Bridge between router and repository for paginated menus."""
        return self.menu_repo.get_active_menu_paginated_by_restaurant(
            restaurant_id=restaurant_id,
            search_query=search_query,
            page=page,
            page_size=page_size
        )

    def get_global_menus(
            self,
            restaurant_id: Optional[str] = None,
            item_name: Optional[str] = None,
            price: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Search for menu globally then apply filter."""
        items = self.menu_repo.get_menu_by_filters(
            restaurant_id=restaurant_id,
            item_name=item_name,
            price=price)

        active_items = [item for item in items if str(item.get('is_available', '')).lower() == 'true']
        
        all_restaurants = self.restaurant_repo.get_all()
        restaurants = {res['id']: res['name'] for res in all_restaurants}

        for item in active_items:
            res_id = item.get('restaurant_id')
            item["restaurant_name"] = restaurants.get(res_id, "Unknown Kitchen")

        return active_items