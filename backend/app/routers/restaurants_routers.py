from typing import Any, Optional, List, Dict
from fastapi import APIRouter, Depends, Query
from app.services.restaurant_services import restaurant_service
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter(tags=["Restaurants"])

def get_restaurant_service():
    return restaurant_service(restaurant_repository())

@router.get("/", response_model=List[Dict[str, Any]])
def browse_restaurants(
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    service: Any = Depends(get_restaurant_service)
):
    """
    Browse restaurants with pagination.
    Returns result.get("data") to satisfy legacy tests expecting a raw list.
    """
    result = service.browse_restaurants(keyword, page, limit)
    return result.get("data", [])
  