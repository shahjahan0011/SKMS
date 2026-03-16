"""Restaurant services module."""
from typing import Dict, List, Any, Optional

from app.storage.repositories.restaurant_repository import restaurant_repository

class restaurant_service:
    """Restaurant service class."""

    def __init__(self, repo):
        """Initialize the restaurant service."""
        self.repo = repo

    def browse_restaurants(self, keyword: Optional[str] = None, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Browse all restaurants."""
        all_restaurants = self.repo.get_menu_by_restaurant()

        result = [r for r in all_restaurants if str(r.get('status', '')).lower() in ['true', '1']]
       
        if keyword:
            clean_keyword = keyword.lower().strip() # FIX: Added () to keyword.lower
            result = [r for r in result if clean_keyword in r.get('name', '').lower()]

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
