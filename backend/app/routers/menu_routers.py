"""Menu routes module."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from app.storage.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(prefix="/menus", tags=["Menus"])

def get_menu_service():
    """Dependency injection for MenuService."""
    return MenuService(MenuRepository(), RestaurantRepository())


@router.get("/{restaurant_id}", response_model=Dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id: str,
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service: MenuService = Depends(get_menu_service)
):
    """Get menu for a specific restaurant with pagination and search."""
    return service.get_active_menu_paginated_by_restaurant(
        restaurant_id=restaurant_id,
        search_query=search,
        page=page,
        page_size=page_size
    )


@router.get("/{restaurant_id}/items/{item_id}", response_model=Dict[str, Any])
def get_menu_item_detail(
    restaurant_id: str,
    item_id: str,
    service: MenuService = Depends(get_menu_service)
):
    """Retrieve detailed information for a specific menu item (FR6)."""
    return service.get_menu_item_details(restaurant_id=restaurant_id, item_id=item_id)


@router.get("/")
def browse_menus(
    restaurant_id: Optional[str] = None,
    item_name: Optional[str] = None,
    price: Optional[float] = None,
    service: MenuService = Depends(get_menu_service)
):
    """Search for menus globally across all restaurants."""
    return service.get_global_menus(
        item_name=item_name,
        price=price,
        restaurant_id=restaurant_id
    )
