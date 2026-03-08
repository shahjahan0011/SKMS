"""Menu services module."""

from ast import Dict, List
from app.storage.repositories.menu_repository import MenuRepository

# pylint: disable=too-few-public-methods
class MenuService:
    """Service class for menu-related operations."""
    def __init__(self, repo: MenuRepository):
        self.menu_repository = repo

    def get_all_menus_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get all menu items for a specific restaurant."""
        return self.menu_repository.get_menu_by_restaurant(restaurant_id)

    def get_active_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Get active menu items for a specific restaurant."""
        all_menus = self.menu_repository.get_menu_by_restaurant(restaurant_id)

        # Filter for active menu items using True of 1 in the 'status' field
        active_menus = [menu for menu in all_menus if str(menu.get('status', '')).lower() in ['true', '1']]

        return active_menus

    def get_menu_item_by_id(self, item_id: str) -> Dict:
        """Get menu item by id."""
        return self.menu_repository.get_menu_item_by_id(item_id)
