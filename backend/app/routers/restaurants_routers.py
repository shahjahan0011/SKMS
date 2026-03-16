'''Restaurants routes module'''

from fastapi import APIRouter
from app.services.restaurant_services import restaurant_service
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(tags=["browse restaurants"])
def get_restaurant_service():
    """Get restaurant service instance."""
    repo = restaurant_repository()
    return restaurant_service(repo)

@router.get("/", response_model=list)
def browse_restaurants(keyword: str = None, page: int = 1, limit: int = 20):
    """Browse all restaurants."""
    service = get_restaurant_service()
    result service.browse_restaurants(keyword, page, limit)
    return result["data"]
