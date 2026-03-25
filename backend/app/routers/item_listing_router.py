from fastapi import APIRouter, HTTPException
from app.services.item_listing_services import item_listing_service
from app.storage.repositories.restaurant_repository import restaurant_repository
from app.storage.repositories.menu_repository import menu_repository

router = APIRouter()

# Repos and services for item listing
res_repo = restaurant_repository()
menu_repo = menu_repository()

listing_service = item_listing_service(
    res_repo,
    menu_repo
)

@router.get("/restaurants")
def get_all_restaurants():
    """Gets all restaurants"""

    return {"data": listing_service.get_all_restaurants()}

@router.get("/restaurants/{restaurant_id}")
def get_restaurant_by_id(restaurant_id: str):
    """Get a restaurant by id"""
    try:
        return listing_service.get_restaurant_by_id(restaurant_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.get("/menu/{item_id}")
def get_menu_item_by_id(item_id: str):
    """Get a specific menu item by its ID."""
    try:
        return listing_service.get_menu_item_by_id(item_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.get("/{restaurant_id}")
def get_restaurant_menu(restaurant_id: str):
    """Get the menu for a specific restaurant"""
    try:
        return listing_service.get_restaurant_menu(restaurant_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
