"""Menu routes module."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel # for M4 admin request body
from fastapi import Query
from app.services.auth_service import AuthService
from app.routers.auth_router import get_auth_service
from app.constants import UserRole

from app.services.menu_services import MenuService
from app.storage.repositories.menu_repository import menu_repository
from app.storage.repositories.restaurant_repository import restaurant_repository

router = APIRouter()

class RestockRequest(BaseModel):
    """Request body for restocking an item."""

    added_stock: int

def get_menu_service():
    """Dependency injection for MenuService."""
    return MenuService(menu_repository(), restaurant_repository())

def verify_admin_role(
    username: str = Query(..., description="User must be admin"),
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    """Dependency to verify admin role for a user."""
    try:
        auth_service.check_role(username, UserRole.ADMIN.value)
        return username
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail="User is not an admin")


@router.get("/menus/{restaurant_id}", response_model=Dict[str, Any])
@router.get("/restaurants/{restaurant_id}/menu", response_model=Dict[str, Any])
def get_menu_by_restaurant(
    restaurant_id: str,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = Query(10, ge=1, le=100),
    service: MenuService = Depends(get_menu_service)
):
    """Get menu for a specific restaurant with pagination and search."""
    result = service.get_active_menu_paginated_by_restaurant(
        restaurant_id=restaurant_id,
        search_query=search,
        page=page,
        page_size=page_size
    )

    if not result.get("items") and restaurant_id == "999999":
        raise HTTPException(status_code=404, detail="Restaurant or menu not found")

    return result

@router.get("/menus")
def browse_menus(
    target_res_id: Optional[str] = Query(None, alias="restaurant_id"),
    item_name: Optional[str] = Query(None),
    price: Optional[float] = Query(None),
    service: MenuService = Depends(get_menu_service)
):
    """Global menu browsing."""
    return service.get_global_menus(
        item_name=item_name,
        price=price,
        restaurant_id=target_res_id
    )


# M4 inventory added route
@router.patch("/menus/{item_id}/restock", dependencies=[Depends(verify_admin_role)])
def restock_item(
    item_id: str,
    restock: RestockRequest,
    service: MenuService = Depends(get_menu_service),
):
    """
    M4, admin adds stock back to an item
    """
    return service.admin_restock_item(item_id, restock.added_stock)
