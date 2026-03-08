"""Menu routes module."""

from fastapi import APIRouter
from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import MenuRepository
from app.schemas.menu_item_schema import MenuItem
from app.services.menu_services import MenuService
from typing import List

router = APIRouter(prefix="/menus", tags=["Menus"])
# Repositories and services for menu routes
def get_menu_service():
    """Get menu service instance."""
    repo = MenuRepository()
    return MenuService(repo)

@router.get("/{restaurant_id}", response_model=List[MenuItem])
def get_menu_by_restaurant(restaurant_id: str):
    """Get menu for a specific restaurant."""
    service = get_menu_service()
    return service.get_all_menus_by_restaurant(restaurant_id)
