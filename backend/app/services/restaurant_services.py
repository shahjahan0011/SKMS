"""Restaurant services module."""

from app.storage.repositories.restaurant_repository import restaurant_repository
from typing import Dict, List, Any

class restaurant_service:
    """Restaurant service class using snake_case naming."""

    
    def __init__(self, repo: restaurant_repository):
        """Initialize the restaurant service."""
        self.repo = repo

        
    def browse_restaurants(self, keyword: str = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Browse all restaurants with filtering and pagination."""
    
        all_restaurants = self.repo.get_all()

        active_restaurants = [
            restaurant for restaurant in all_restaurants
            if str(restaurant.get('is_active', '')).lower() in ['true', '1', 'yes']
        ]

        result = active_restaurants
        if keyword:
            keyword_clean = keyword.lower().strip()
            result = [
                r for r in active_restaurants 
                if keyword_clean in r.get('name', '').lower()
            ]

        if not result:
            return {
                "metadata": {
                    "total_items": 0,
                    "total_pages": 0,
                    "current_page": page,
                    "items_per_page": limit
                },
                "data": [],
                "message": "No restaurants found matching the keyword."
            }

        total_items = len(result)
        total_pages = (total_items + limit - 1) // limit

        start = (page - 1) * limit
        end = start + limit
        paginated_result = result[start:end]

        return {
            "metadata": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "items_per_page": limit,
                "has_next_page": page < total_pages
            },
            "data": paginated_result
        }