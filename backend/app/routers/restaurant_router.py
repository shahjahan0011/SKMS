from typing import Any, Optional, List, Dict
from fastapi import APIRouter, Depends, Query
from app.services.restaurant_service import RestaurantService
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(tags=["Restaurants"])

def get_restaurant_service():
    return RestaurantService(restaurant_repository())

@router.get("/", response_model=Dict[str, Any])
def browse_restaurants(
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    service: RestaurantService = Depends(get_restaurant_service)
):
    result = service.browse_restaurants(keyword=keyword, page=page, limit=limit)

    return result
