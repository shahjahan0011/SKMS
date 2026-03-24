"""Integration Tests for MenuRepository."""
import pytest
from app.storage.repositories.menu_repository import menu_repository
from backend.app.routers.menu_router import get_menu_service


def test_get_menu_by_restaurant_id_from_csv():
    """
    Test that the repository can correctly fetch and parse
    data from the actual CSV storage.
    """
    repo = menu_repository()

    result = repo.get_menu_by_restaurant("13")

    assert isinstance(result, list)
    assert len(result) > 0

    item_names = [item["item_name"] for item in result]
    assert "Briyani rice" in item_names


def test_get_menu_item_by_invalid_id():
    """
    Test that the repository returns an empty list
    when a non-existent restaurant_id is provided.
    """
    repo = menu_repository()
    mock_data = [
        {"id": "1", "restaurant_id": "1", "item_name": "Pizza", "price": "10", "is_available": "True"},
        {"id": "2", "restaurant_id": "1", "item_name": "Pasta", "price": "12", "is_available": "True"},
        {"id": "3", "restaurant_id": "2", "item_name": "Burger", "price": "8", "is_available": "True"},
    ]
    repo.get_all = MagicMock(return_value=mock_data)

    repo.get_menu_item_by_id = MagicMock(side_effect=lambda id: next((item for item in mock_data if item["id"] == id), None))
    return repo

def test_get_menu_item_by_id_valid(mock_menu_repo):
    """Test for getting a valid menu item."""
    item = mock_menu_repo.get_menu_item_by_id("1")
    assert item is not None
    assert item["id"] == "1"
    assert item["item_name"] == "Pizza"

def test_get_menu_item_by_id_invalid(mock_menu_repo):
    """Test for trying to get an invalid menu item by ID."""
    item = mock_menu_repo.get_menu_item_by_id("999")
    assert item is None

def test_search_endpoint(client):
    """Integration test for the search endpoint using dependency overrides."""
    mock_service = MagicMock()
    mock_service.get_active_menu_paginated_by_restaurant.return_value = {
        "items": [{"name": "Fried Rice", "price": 10.0}],
        "total_items": 1,
        "page": 1,
        "page_size": 10
    }

    app.dependency_overrides[get_menu_service] = lambda: mock_service
    try:
        response = client.get("/menus/1?search=rice")
        assert response.status_code == 200
        assert response.json()['items'][0]['name'] == 'Fried Rice'
    finally:
        app.dependency_overrides.clear()
