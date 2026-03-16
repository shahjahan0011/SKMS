"""Restaurant services module."""

from importlib import metadata
from app.storage.repositories.restaurant_repository import RestaurantRepository
from typing import Dict, List

class RestaurantService:
    """Restaurant service class."""

    def __init__(self, repo: RestaurantRepository):
        """Initialize the restaurant service."""
        self.repo = repo

    def browse_restaurants(self, keyword: str = None, page: int = 1, limit: int = 20) -> List[Dict]:
        """Browse all restaurants."""

        all_restaurants = self.repo.get_all_restaurants()

        result = [
            restaurant for restaurant in all_restaurants
            if str(restaurant.get('is_active', '')).lower() in ['true', '1']
            ]

        if keyword:
            keyword = keyword.lower().strip()
            result = [restaurant for restaurant in result if keyword.lower() in restaurant.get('name', '').lower()]

        if not result:
            return {"message": "No restaurants found matching the keyword."}

        total_items = len(result)
        total_pages = (total_items + limit - 1)

        start = (page - 1) * limit
        end = start + limit
        paginated_result = result[start:end]

        return {
            metadata: {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": limit,
                "has_next_page": page < total_pages
            },
            "data": paginated_result
        }
