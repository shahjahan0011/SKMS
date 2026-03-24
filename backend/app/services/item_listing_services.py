"""Item listing Services"""

from app.storage.repositories.restaurant_repository import restaurant_repository
from app.storage.repositories.menu_repository import menu_repository


class item_listing_service:
    """
    Service for Item Listing from Menu
    """

    def __init__(self, restaurant_repo: restaurant_repository, menu_repo: menu_repository):
        self.restaurant_repo = restaurant_repo
        self.menu_repo = menu_repo



    def _validate_restaurant_exists(self, restaurant_id: str):
        """this method checks if a restaurant is valid"""
        restaurants = self.restaurant_repo.get_all_restaurants()

        for r in restaurants:
            if r["id"] == restaurant_id:
                return restaurants

        raise ValueError("Invalid Restaurant")
    


    def _validate_menu_items(self, menu_items, restaurants):
        """checks if menu items belong to a valid restaurant"""
        restaurant_ids = [r["id"] for r in restaurants]

        for item in menu_items:
            if item["restaurant_id"] not in restaurant_ids:
                raise ValueError("Menu Item references an Invalid Restaurant")
        


    def get_all_restaurants(self) -> list:
        """returns all restaurants"""
        return self.restaurant_repo.get_all_restaurants()



    def get_restaurant_menu(self, restaurant_id: str) -> list:
        """returns menu items for a restaurant using the restaurant id"""
        restaurants = self._validate_restaurant_exists(restaurant_id)

        menu_items = self.menu_repo.get_menu_by_restaurant(restaurant_id)
        self._validate_menu_items(menu_items, restaurants)

        return menu_items



    def get_restaurant_by_id(self, restaurant_id: str):
        """getter for the restaurant by the restaurant id"""
        restaurant = self.restaurant_repo.get_restaurant_by_id(restaurant_id)

        if not restaurant:
            raise ValueError("Ivalid Restaurant")

        return restaurant



    def get_menu_item_by_id(self, item_id: str):
        """getter for the menu item but menu item id"""
        item = self.menu_repo.get_menu_item_by_id(item_id)

        if not item:
            raise ValueError("Invalid Menu Item")

        return item
