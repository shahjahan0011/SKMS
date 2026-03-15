"""Item listing Services"""

from app.storage.repositories.restaurant_repository import restaurant_repository
from app.storage.repositories.menu_repository import menu_repository


class item_listing_service:
    """
    Service for Item Listing from Menu
    """

    def __init__(self, restaurant_repo, menu_repo):
        self.restaurant_repo = restaurant_repo
        self.menu_repo = menu_repo

    def get_all_restaurants(self) -> list:
        """Returns all restaurants"""
        return self.restaurant_repo.get_all_restaurants()

    def get_restaurant_menu(self, restaurant_id: str) -> list:
        """Return menu items for a given restaurant"""
        restaurants = self.restaurant_repo.get_all_restaurants()

        exists = any(r["id"] == restaurant_id for r in restaurants)

        if not exists:
            raise ValueError("Restaurant not found")

        menu_items = self.menu_repo.get_menu_by_restaurant(restaurant_id)
        restaurant_ids = {r["id"] for r in restaurants}

        for item in menu_items:
            if item["restaurant_id"] not in restaurant_ids:
                raise ValueError("Menu item references invalid restaurant")

        return menu_items

    def get_restaurant_by_id(self, restaurant_id: str):
        """Get a restaurant by its id"""
        restaurant = self.restaurant_repo.get_restaurant_by_id(restaurant_id)

        if restaurant is None:
            raise ValueError("Restaurant not found")

        return restaurant

    def get_menu_item_by_id(self, item_id: str):
        """Get a menu item by menu item id"""
        item = self.menu_repo.get_menu_item_by_id(item_id)

        if item is None:
            raise ValueError("Menu item not found")

        return item
