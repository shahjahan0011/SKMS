import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@patch("app.services.restaurant_service.RestaurantService.browse_restaurants")
def test_router_passes_params_to_service(mock_browse):

    mock_browse.return_value = {
        "metadata": {"total_items": 1},
        "data": [{"name": "Mock Pizza", "is_active": "true"}]
    }

    response = client.get("/restaurants/?keyword=Pizza&page=2&limit=5")

    assert response.status_code == 200
    mock_browse.assert_called_once_with(keyword="Pizza", page=2, limit=5)


@patch("app.services.restaurant_service.RestaurantService.browse_restaurants")
def test_get_restaurants_success_structure(mock_browse):

    mock_browse.return_value = {
        "metadata": {"total_items": 1},
        "data": [{"name": "Mock Pasta", "is_active": "true"}]
    }

    response = client.get("/restaurants/")

    assert response.status_code == 200
    data = response.json()
    assert "metadata" in data
    assert data["data"][0]["name"] == "Mock Pasta"
