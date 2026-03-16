"""Restaurant services module."""
from typing import Dict, List, Any, Optional
from app.storage.repositories.restaurant_repository import restaurant_repository

class RestaurantService:
    """Restaurant service class."""

    def __init__(self, repo: restaurant_repository):
        """Initialize the restaurant service."""
        self.repo = repo

    def browse_restaurants(self, keyword: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Browse all restaurants with filtering and pagination."""

        all_restaurants = self.repo.get_menu_by_restaurant()

        active_restaurants = [
            r for r in all_restaurants 
            if str(r.get('status', r.get('is_active', ''))).lower() in ['true', '1', 'yes']
        ]

        result = active_restaurants
        if keyword:
            keyword_clean = keyword.lower().strip()
            result = [
                r for r in active_restaurants 
                if keyword_clean in r.get('name', '').lower()
            ]

        total_items = len(result)
        total_pages = (total_items + limit - 1) // limit if limit > 0 else 1

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