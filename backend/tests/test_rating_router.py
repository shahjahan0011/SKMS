import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routers import rating_router

client = TestClient(app)


def test_create_rating_route(monkeypatch):
    """Test POST /ratings endpoint"""
    
    def mock_create_rating(order_id, restaurant_id, username, score, comment):
        return {
            "rating_id": "r1",
            "order_id": order_id,
            "restaurant_id": restaurant_id,
            "username": username,
            "score": score,
            "comment": comment,
            "created_at": "2026-03-24T10:00:00",
        }
    
    monkeypatch.setattr(rating_router, "create_rating", mock_create_rating)
    
    response = client.post(
        "/ratings/",
        json={
            "order_id": "o1",
            "restaurant_id": "rest_1",
            "username": "jahan",
            "score": 5,
            "comment": "Great!"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["score"] == 5
    assert data["comment"] == "Great!"


def test_get_rating_route(monkeypatch):
    """Test GET /ratings/{rating_id} endpoint"""
    
    def mock_get_rating(rating_id):
        return {
            "rating_id": rating_id,
            "score": "4",
            "comment": "Good"
        }
    
    monkeypatch.setattr(rating_router, "get_rating", mock_get_rating)
    
    response = client.get("/ratings/r1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["rating_id"] == "r1"


def test_get_restaurant_stats_route(monkeypatch):
    """Test GET /ratings/restaurant/{id}/stats endpoint"""
    
    def mock_stats(restaurant_id):
        return {
            "restaurant_id": restaurant_id,
            "average_rating": 4.5,
            "total_ratings": 10,
            "rating_breakdown": {1: 0, 2: 1, 3: 2, 4: 4, 5: 3}
        }
    
    monkeypatch.setattr(rating_router, "get_restaurant_rating_stats", mock_stats)
    
    response = client.get("/ratings/restaurant/rest_1/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert data["average_rating"] == 4.5
    assert data["total_ratings"] == 10