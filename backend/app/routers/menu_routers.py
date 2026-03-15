"""Menu routes module."""

from fastapi import APIRouter, Query
from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from typing import Any

router = APIRouter(prefix="/menus", tags=["Menus"])
# Repositories and services for menu routes
def get_menu_service():
    """Get menu service instance."""
    repo = MenuRepository()
    return MenuService(repo)

@router.get("/{restaurant_id}", response_model=dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id: str,
    search: str = Query(None, description="Search query for menu items"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page")
) -> dict[str, Any]:

    """Get menu for a specific restaurant."""
    service = get_menu_service()
    return service.get_active_menu_paginated_by_restaurant(
        restaurant_id=restaurant_id,
        search_query=search,
        page=page,
        page_size=page_size
    )
