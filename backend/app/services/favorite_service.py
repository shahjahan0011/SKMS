"""User's Favorite Service"""

from app.storage.repositories.favorite_repository import favorite_repository
from app.storage.repositories.restaurant_repository import restaurant_repository as RestaurantRepo


class favorite_service:
    """
    Service for User Favorites
    """

    def __init__(self):
        self.repo = favorite_repository
        self.restaurant_repo = RestaurantRepo()



    def add_favorite(self, user_id, restaurant_id):
        """adds a restaurant to user favorites"""

        restaurant = self.restaurant_repo.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            raise ValueError("restaurant not found")

        self.repo.add_favorite(user_id, restaurant_id)



    def remove_favorite(self, user_id, restaurant_id):
        """removes a restaurant from user favorites"""

        self.repo.remove_favorite(user_id, restaurant_id)



    def get_user_favorites(self, user_id):
        """returns favorite restaurants for a user"""

        favorites = self.repo.get_user_favorites(user_id)

        result = []

        for fav in favorites:
            restaurant = self.restaurant_repo.get_restaurant_by_id(int(fav["restaurant_id"]))
            if restaurant:
                result.append(restaurant)

        return result


favorite_service = favorite_service()