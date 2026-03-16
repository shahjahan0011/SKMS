'''Restaurants routes module'''

from fastapi import APIRouter
from app.services.restaurant_services import restaurant_service
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(tags=["browse restaurants"])

def get_restaurant_service():
    """Get restaurant service instance using snake_case factory functions."""
    repo = restaurant_repository()
    return restaurant_service(repo)

@router.get("/", response_model=dict)
def browse_restaurants(keyword: str = None, page: int = 1, limit: int = 20):
    """Browse all restaurants."""
    service = get_restaurant_service()
    return service.browse_restaurants(keyword, page, limit)