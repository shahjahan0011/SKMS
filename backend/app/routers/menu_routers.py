"""Menu routes module."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from app.storage.repositories.restaurant_repository import RestaurantRepository

# We keep the prefix here if it's not already in main.py
router = APIRouter(prefix="/menus", tags=["Menus"])

def get_menu_service():
    """Dependency injection for MenuService."""
    return MenuService(MenuRepository(), RestaurantRepository())

@router.get("/{restaurant_id}", response_model=Dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id: str,
    search: Optional[str] = Query(None, description="Search query for menu items"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    service: MenuService = Depends(get_menu_service)
):
    """Get menu for a specific restaurant with pagination and search."""
    return service.get_active_menu_paginated_by_restaurant(
        restaurant_id=restaurant_id,
        search_query=search,
        page=page,
        page_size=page_size
    )

@router.get("/")
def browse_menus(
    restaurant_id: Optional[str] = Query(None, description="Filter by restaurant ID"),
    item_name: Optional[str] = Query(None, description="Search by item name"),
    price: Optional[float] = Query(None, description="Filter by max price"),
    service: MenuService = Depends(get_menu_service)
):
    """Global menu browsing."""
    return service.get_global_menus(
        item_name=item_name,
        price=price,
        restaurant_id=restaurant_id
    )