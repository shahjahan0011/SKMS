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

    