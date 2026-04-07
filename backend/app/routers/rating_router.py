from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.schemas.rating_schema import CreateRatingRequest
from app.services.rating_service import (
    create_rating,
    get_rating,
    update_rating_comment,
    delete_rating_by_user,
    get_restaurant_rating_stats,
    get_user_ratings,
)

router = APIRouter(prefix="/ratings", tags=["Ratings"])

class UpdateRatingCommentRequest(BaseModel):
    username: str
    comment: str


@router.post("/")
def create_new_rating(payload: CreateRatingRequest):
    """
    Create a rating for a delivered order.
    
    - Order must be delivered
    - Order can only be rated once
    - Only order owner can rate
    
    Example:
    {
        "order_id": "o1",
        "restaurant_id": "rest_1",
        "username": "jahan",
        "score": 5,
        "comment": "Great food!"
    }
    """
    return create_rating(
        order_id=payload.order_id,
        restaurant_id=payload.restaurant_id,
        username=payload.username,
        score=payload.score.value,  # ✅ Extract enum value
        comment=payload.comment,
    )


@router.get("/{rating_id}")
def get_rating_endpoint(rating_id: str):
    """Get a specific rating by ID."""
    return get_rating(rating_id)


@router.patch("/{rating_id}/comment")
def update_rating_endpoint(rating_id: str, payload: UpdateRatingCommentRequest):
    """
    Update rating comment (author only).
    
    Example:
    {
        "username": "jahan",
        "comment": "Actually amazing!"
    }
    """
    return update_rating_comment(
        rating_id=rating_id,
        username=payload.username,
        comment=payload.comment,
    )


@router.delete("/{rating_id}")
def delete_rating_endpoint(rating_id: str, username: str = Query(...)):
    """
    Delete a rating (author only).
    
    Query param: ?username=jahan
    """
    delete_rating_by_user(rating_id, username)
    return {"message": "Rating deleted successfully"}


@router.get("/restaurant/{restaurant_id}/stats")
def get_restaurant_stats(restaurant_id: str):
    """
    Get rating statistics for a restaurant.
    
    Returns:
    - average_rating: Average score
    - total_ratings: Number of ratings
    - rating_breakdown: Count of each 1-5 star rating
    
    Example response:
    {
        "restaurant_id": "rest_1",
        "average_rating": 4.5,
        "total_ratings": 10,
        "rating_breakdown": {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    }
    """
    return get_restaurant_rating_stats(restaurant_id)


@router.get("/user/{username}/all")
def get_user_ratings_endpoint(username: str):
    """Get all ratings by a user."""
    return get_user_ratings(username)