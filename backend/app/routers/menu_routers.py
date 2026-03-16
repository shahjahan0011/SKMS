"""Menu routes module."""
feature-menu-detail-FR6
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from app.storage.repositories.restaurant_repository import RestaurantRepository

router = APIRouter(tags=["Menus"])

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
    return service.get_global_menus(
        item_name=item_name,
        price=price,
        restaurant_id=restaurant_id
    )


from fastapi import APIRouter, Query
from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from typing import Any

router = APIRouter(prefix="/menus", tags=["Menus"])

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
    return service.get_paginated_menu_by_restaurant(
        restaurant_id=restaurant_id,
        search=search,
        page=page,
        page_size=page_size
    )

