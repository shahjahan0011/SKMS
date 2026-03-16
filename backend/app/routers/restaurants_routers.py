'''Restaurants routes module'''

from fastapi import APIRouter
from app.services.restaurant_services import RestaurantService
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(prefix="/restaurants", tags=["browse restaurants"])
# Repositories and services for restaurant routes
def get_restaurant_service():
    """Get restaurant service instance."""
    repo = restaurant_repository()
    return RestaurantService(repo)

# The browse_restaurants endpoint allows clients to retrieve a list of restaurants
@router.get("/", response_model=dict)
def browse_restaurants(keyword: str = None, page: int = 1, limit: int = 20):
    """Browse all restaurants."""
    service = get_restaurant_service()
    return service.browse_restaurants(keyword, page, limit)
