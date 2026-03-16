"""Menu routes module."""

from fastapi import APIRouter, Query, Depends
from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import menu_repository
from typing import Any

def get_menu_service():
    """Get menu service instance."""
    repo = menu_repository()
    return MenuService(repo)

@router.get("/{restaurant_id}", response_model=Dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id:str,
    search: str = Query(None, description="Search query for menu items"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    service: MenuService = Depends(get_menu_service)
):
    """Get menu for a specific restaurant."""
    service = get_menu_service()
    return service.get_paginated_menu_by_restaurant(
        restaurant_id=restaurant_id,
        search=search,
        page=page,
        page_size=page_size
    )

@router.get("/")
def browse_menus(
    restaurant_id: Optional[str] = Query(None, description="Filter menu items by restaurant ID"),
    item_name: Optional[str]= Query(None, description="Search query for menu items"),
    price: Optional[float] = Query(None, description="Filter menu items by max_price"),
):
    service = get_menu_service()

    return service.get_global_menus(
        item_name=item_name,
        price=price,
        restaurant_id=restaurant_id
        )
