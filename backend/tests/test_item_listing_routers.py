"""Test for Item Listing Routers"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_all_restaurants():
    """Test for GET /restaurants endpoint"""
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_get_restaurant_by_id_valid():
    """Test for GET /restaurants/{restaurant_id} endpoint for valid id"""
    response = client.get("/restaurants/1")

    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_get_restaurant_by_id_invalid():
    """Test for GET /restaurants/{restaurant_id} endpoint for invalid id"""
    response = client.get("/restaurants/999999")

    assert response.status_code == 404

def test_get_restaurant_menu_valid():
    """Test for GET /restaurants/{restaurant_id}/menu endpoint with valid id"""
    response = client.get("/restaurants/1/menu")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_restaurant_menu_invalid():
    """Test for GET /restaurants/{restaurant_id}/menu endpoint with invalid id"""
    response = client.get("/restaurants/999999/menu")

    assert response.status_code == 404

def test_get_menu_item_by_id_valid():
    """Test for GET /menu/{item_id} endpoint with valid id"""
    response = client.get("/menu/1")

    assert response.status_code == 200
    assert response.json()["id"] == "1"

def test_get_menu_item_by_id_invalid():
    """Test for GET /menu/{item_id} endpoint with invalid id"""
    response = client.get("/menu/999999")

    assert response.status_code == 404
