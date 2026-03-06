"""Restaurant services module."""
from importlib import metadata
from sympy import limit

from sympy import limit

from repositories.restaurant_repository import RestaurantRepository
from typing import Dict, List



class RestaurantService:
    """Restaurant service class."""

    def _init__(self, repo: RestaurantRepository):
        """Initialize the restaurant service."""
        self.repo = repo

    def browse_restaurants(self, keyword: str = None, page: int = 1, limit: int = 20) -> List[Dict]:
        """Browse all restaurants."""
        all_restaurants =  self.repo.get_all_restaurants()  

        # Filter for active restaurants using True of 1 in the 'status' field
        result = [restaurant for restaurant in all_restaurants if str(restaurant.get('status', '')).lower() in ['true', '1']]

        # If a keyword is provided, filter the restaurants by name
        if keyword:
            keyword = keyword.lower.strip()
            result = [restaurant for restaurant in result if keyword.lower() in restaurant.get('name', '').lower()]


         # handle empty list of result after filtering by keyword return graceful message
        if not result:
            return {"message": "No restaurants found matching the keyword."}   

        # Calculate total items and total pages for pagination
        total_items = len(result) 
        total_pages = (total_items + limit - 1)

        # Implement pagination
        start = (page - 1) * limit
        end = start + limit
        paginated_result = result[start:end]

        #return paginated result with total items and total pages for better client handling of pagination
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

   
