"""Item listing Services"""

from app.storage.repositories.restaurant_repository import RestaurantRepository
from app.storage.repositories.menu_repository import MenuRepository


class ItemListingService:
    """
    Service for Item Listing from Menu
    """

    def __init__(self, restaurant_repo: RestaurantRepository, menu_repo: MenuRepository):
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

        return self.menu_repo.get_by_restaurant(restaurant_id)