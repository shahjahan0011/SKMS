"""Menu routes module."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import menu_repository
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter()

def get_menu_service():
    """Dependency injection for MenuService."""
    return MenuService(menu_repository(), restaurant_repository())

@router.get("/menus/{restaurant_id}", response_model=Dict[str, Any])
@router.get("/restaurants/{restaurant_id}/menu", response_model=Dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id: str,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = Query(10, le=100),
    service: MenuService = Depends(get_menu_service)
):
    """Get menu for a specific restaurant with pagination and search."""
    
    return service.get_active_menu_paginated_by_restaurant(
        restaurant_id=restaurant_id,
        search_query=search,
        page=page,
        page_size=page_size
    )

if not result.get("items"):
    raise HTTPException(status_code=404, detail="Restaurant or menu not found")
return result
