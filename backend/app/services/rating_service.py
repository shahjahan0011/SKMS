from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException

from app.storage.repositories.rating_repository import (
    save_rating,
    get_rating_by_id,
    get_rating_by_order,
    get_ratings_by_restaurant,
    get_ratings_by_user,
    update_rating,
    delete_rating,
)
from app.storage.repositories.order_repository import get_order_by_id


def _now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def _validate_order_delivered(order: dict) -> None:
    """Validate that order is delivered before allowing rating."""
    if order.get("status") != "delivered":
        raise HTTPException(
            status_code=400,
            detail="Only delivered orders can be rated"
        )


def _validate_not_already_rated(order_id: str) -> None:
    """Validate that order hasn't been rated already."""
    existing = get_rating_by_order(order_id)
    if existing:
        raise HTTPException(
            status_code=409,
            detail="This order has already been rated"
        )


def create_rating(
    order_id: str,
    restaurant_id: str,
    username: str,
    score: int,
    comment: str = ""
) -> dict:
    """
    Create a rating for a delivered order.
    
    Args:
        order_id: Order being rated
        restaurant_id: Restaurant being rated
        username: User rating
        score: Rating score 1-5
        comment: Optional comment
        
    Returns:
        Created rating dict
    """
    # Validate order exists and is delivered
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    _validate_order_delivered(order)
    _validate_not_already_rated(order_id)
    
    # Validate score
    if not 1 <= score <= 5:
        raise HTTPException(
            status_code=400,
            detail="Rating score must be between 1 and 5"
        )
    
    # Validate order belongs to user
    if order.get("username") != username:
        raise HTTPException(
            status_code=403,
            detail="You can only rate your own orders"
        )
    
    # Validate restaurant matches order
    if order.get("restaurant_id") != restaurant_id:
        raise HTTPException(
            status_code=400,
            detail="Restaurant ID doesn't match order"
        )
    
    rating = {
        "rating_id": str(uuid4()),
        "order_id": order_id,
        "restaurant_id": restaurant_id,
        "username": username,
        "score": str(score),
        "comment": comment.strip()[:500],  # Limit comment length
        "created_at": _now_iso(),
    }
    
    return save_rating(rating)


def get_rating(rating_id: str) -> dict:
    """Get a specific rating."""
    rating = get_rating_by_id(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


def update_rating_comment(rating_id: str, username: str, comment: str) -> dict:
    """
    Update rating comment (only author can update).
    
    Args:
        rating_id: Rating to update
        username: User making the update
        comment: New comment
        
    Returns:
        Updated rating
    """
    rating = get_rating_by_id(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    if rating.get("username") != username:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own ratings"
        )
    
    rating["comment"] = comment.strip()[:500]
    rating["updated_at"] = _now_iso()
    
    updated = update_rating(rating)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update rating")
    
    return updated


def delete_rating_by_user(rating_id: str, username: str) -> None:
    """
    Delete a rating (only author can delete).
    
    Args:
        rating_id: Rating to delete
        username: User making the deletion
    """
    rating = get_rating_by_id(rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    if rating.get("username") != username:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own ratings"
        )
    
    success = delete_rating(rating_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete rating")


def get_restaurant_rating_stats(restaurant_id: str) -> dict:
    """
    Calculate rating statistics for a restaurant.
    
    Args:
        restaurant_id: Restaurant to get stats for
        
    Returns:
        Dict with average rating, total ratings, and breakdown
    """
    ratings = get_ratings_by_restaurant(restaurant_id)
    
    if not ratings:
        return {
            "restaurant_id": restaurant_id,
            "average_rating": 0.0,
            "total_ratings": 0,
            "rating_breakdown": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    
    # Calculate breakdown
    breakdown = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    total_score = 0
    
    for rating in ratings:
        score = int(rating.get("score", 0))
        if 1 <= score <= 5:
            breakdown[score] += 1
            total_score += score
    
    average = round(total_score / len(ratings), 2) if ratings else 0.0
    
    return {
        "restaurant_id": restaurant_id,
        "average_rating": average,
        "total_ratings": len(ratings),
        "rating_breakdown": breakdown
    }


def get_user_ratings(username: str) -> list[dict]:
    """Get all ratings by a user."""
    return get_ratings_by_user(username)