"""Test for Item Listing Routers"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_all_restaurants():
    """Test for GET /restaurants endpoint"""
    response = client.get("/restaurants")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
