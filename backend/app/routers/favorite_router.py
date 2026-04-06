"""Router for favorite endpoints"""

from fastapi import APIRouter, HTTPException

from app.services.favorite_service import favorite_service

router = APIRouter()
favorite_service = favorite_service



@router.post("/favorites")
def add_favorite(user_id: int, restaurant_id: int):
    """add a restaurant to favorites"""

    try:
        favorite_service.add_favorite(user_id, restaurant_id)
        return {"message": "favorite added"}

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))



@router.delete("/favorites")
def remove_favorite(user_id: int, restaurant_id: int):
    """remove a restaurant from favorites"""

    favorite_service.remove_favorite(user_id, restaurant_id)
    return {"message": "favorite removed"}



@router.get("/favorites/user/{user_id}")
def get_user_favorites(user_id: int):
    """get favorites for a user"""

    return favorite_service.get_user_favorites(user_id)
