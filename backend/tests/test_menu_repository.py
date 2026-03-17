"""Tests for MenuRepository."""

import pytest
from unittest.mock import MagicMock
from app.main import app
from app.storage.repositories.menu_repository import menu_repository
from app.routers.menu_routers import get_menu_service

@pytest.fixture
def mock_menu_repo():
    """Fixture for menu_repository with mock data."""
    repo = menu_repository()
    mock_data = [
        {"id": "1", "restaurant_id": "1", "item_name": "Pizza", "price": "10", "is_available": "True"},
        {"id": "2", "restaurant_id": "1", "item_name": "Pasta", "price": "12", "is_available": "True"},
        {"id": "3", "restaurant_id": "2", "item_name": "Burger", "price": "8", "is_available": "True"},
    ]
    repo.get_all = MagicMock(return_value=mock_data)
    # Mock the method to return None for invalid IDs
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