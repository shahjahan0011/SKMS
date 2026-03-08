"""Test for Item Listing Routers"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_all_restaurants():
    """Test for GET /restaurants endpoint"""
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_restaurant_by_id_valid():
    """Test for GET /restaurants/{restaurant_id} endpoint for valid id"""
    response = client.get("/restaurants/1")

    assert response.status_code == 200
    assert response.json()["id"] == "1"
