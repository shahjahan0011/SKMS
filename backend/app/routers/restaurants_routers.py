from typing import Any, Optional, List, Dict
from fastapi import APIRouter, Depends, Query
from app.services.restaurant_services import RestaurantService
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(tags=["Restaurants"])

def get_restaurant_service():
    return RestaurantService(restaurant_repository())

@router.get("/", response_model=List[Dict[str, Any]])
def browse_restaurants(
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    service: RestaurantService = Depends(get_restaurant_service)
):
    """Browse restaurants with pagination, returning a list for legacy test support."""
    result = service.browse_restaurants(keyword, page, limit)
    
    return result.get("data", [])
