from pydantic import BaseModel, Field
from enum import Enum


class RatingScore(int, Enum):
    """Rating scores from 1-5 stars"""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class CreateRatingRequest(BaseModel):
    """Request body for creating a rating"""
    order_id: str = Field(..., min_length=1, description="Order being rated")
    restaurant_id: str = Field(..., min_length=1, description="Restaurant being rated")
    username: str = Field(..., min_length=1, description="User rating")
    score: RatingScore = Field(..., description="Rating score 1-5")
    comment: str = Field(default="", max_length=500, description="Optional comment")


class RatingResponse(BaseModel):
    """Response body for rating"""
    rating_id: str
    order_id: str
    restaurant_id: str
    username: str
    score: int
    comment: str
    created_at: str


class RestaurantRatingStats(BaseModel):
    """Restaurant rating statistics"""
    restaurant_id: str
    restaurant_name: str
    average_rating: float
    total_ratings: int
    rating_breakdown: dict  # {1: count, 2: count, ...}