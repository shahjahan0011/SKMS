import pytest
from app.storage.repositories.rating_repository import (
    save_rating,
    get_rating_by_id,
    get_all_ratings,
    get_ratings_by_restaurant,
    get_ratings_by_user,
    get_rating_by_order,
    update_rating,
    delete_rating,
)


def test_save_rating_success():
    """Test saving a rating"""
    rating = {
        "rating_id": "r1",
        "order_id": "o1",
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "5",
        "comment": "Great food!",
        "created_at": "2026-03-24T10:00:00",
    }
    
    result = save_rating(rating)
    
    assert result["rating_id"] == "r1"
    assert result["score"] == "5"
    assert result["comment"] == "Great food!"


def test_get_rating_by_id():
    """Test retrieving rating by ID"""
    rating = {
        "rating_id": "r2",
        "order_id": "o2",
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "4",
        "comment": "Good",
        "created_at": "2026-03-24T10:00:00",
    }
    
    save_rating(rating)
    retrieved = get_rating_by_id("r2")
    
    assert retrieved is not None
    assert retrieved["rating_id"] == "r2"
    assert retrieved["score"] == "4"


def test_get_ratings_by_restaurant():
    """Test getting all ratings for a restaurant"""
    save_rating({
        "rating_id": "r3",
        "order_id": "o3",
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "5",
        "comment": "",
        "created_at": "2026-03-24T10:00:00",
    })
    
    save_rating({
        "rating_id": "r4",
        "order_id": "o4",
        "restaurant_id": "rest_1",
        "username": "user2",
        "score": "4",
        "comment": "",
        "created_at": "2026-03-24T10:00:00",
    })
    
    save_rating({
        "rating_id": "r5",
        "order_id": "o5",
        "restaurant_id": "rest_2",
        "username": "user3",
        "score": "3",
        "comment": "",
        "created_at": "2026-03-24T10:00:00",
    })
    
    rest_1_ratings = get_ratings_by_restaurant("rest_1")
    
    assert len(rest_1_ratings) >= 2
    assert all(r.get("restaurant_id") == "rest_1" for r in rest_1_ratings)


def test_get_ratings_by_user():
    """Test getting all ratings by a user"""
    save_rating({
        "rating_id": "r6",
        "order_id": "o6",
        "restaurant_id": "rest_1",
        "username": "test_user",
        "score": "5",
        "comment": "",
        "created_at": "2026-03-24T10:00:00",
    })
    
    user_ratings = get_ratings_by_user("test_user")
    
    assert len(user_ratings) >= 1
    assert all(r.get("username") == "test_user" for r in user_ratings)


def test_get_rating_by_order():
    """Test getting rating by order ID"""
    order_id = "unique_order_123"
    save_rating({
        "rating_id": "r7",
        "order_id": order_id,
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "5",
        "comment": "Excellent!",
        "created_at": "2026-03-24T10:00:00",
    })
    
    rating = get_rating_by_order(order_id)
    
    assert rating is not None
    assert rating["order_id"] == order_id


def test_update_rating():
    """Test updating a rating"""
    save_rating({
        "rating_id": "r8",
        "order_id": "o8",
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "3",
        "comment": "OK",
        "created_at": "2026-03-24T10:00:00",
    })
    
    updated = update_rating({
        "rating_id": "r8",
        "comment": "Actually pretty good!",
    })
    
    assert updated is not None
    assert updated["comment"] == "Actually pretty good!"


def test_delete_rating():
    """Test deleting a rating"""
    save_rating({
        "rating_id": "r9",
        "order_id": "o9",
        "restaurant_id": "rest_1",
        "username": "user1",
        "score": "2",
        "comment": "Bad",
        "created_at": "2026-03-24T10:00:00",
    })
    
    success = delete_rating("r9")
    
    assert success is True
    assert get_rating_by_id("r9") is None