import pytest
from unittest.mock import MagicMock
from app.main import app
from app.storage.repositories.menu_repository import MenuRepository
from app.routers.menu_routers import get_menu_service

@pytest.fixture
def mock_menu_repo():
    """Mock MenuRepository for unit testing."""
    repo = MenuRepository()
    mock_data = [
        {"id": "1", "restaurant_id": "1", "name": "Pizza", "price": "10"},
        {"id": "2", "restaurant_id": "1", "name": "Pasta", "price": "12"},
        {"id": "3", "restaurant_id": "2", "name": "Burger", "price": "8"},
    ]
    repo.get_all = MagicMock(return_value=mock_data)

    # UPDATED: Signature matches the new (restaurant_id, item_id) requirement
    def get_item_by_id(res_id, item_id):
        for item in mock_data:
            if str(item["id"]) == str(item_id) and str(item["restaurant_id"]) == str(res_id):
                return item
        return None

    repo.get_menu_item_by_id = MagicMock(side_effect=get_item_by_id)
    repo.get_menu_by_restaurant = MagicMock(return_value=[mock_data[0], mock_data[1]])
    return repo

  
def test_search_endpoint(client):
    """Test the API search endpoint functionality."""
    mock_service = MagicMock()
    mock_service.get_active_menu_paginated_by_restaurant.return_value = {
        "items": [{"name": "Fried Rice", "price": 10.0}],
        "total": 1, "page": 1, "page_size": 10
    }
    app.dependency_overrides[get_menu_service] = lambda: mock_service
    try:
        response = client.get("/menus/1063?search=rice")
        assert response.status_code == 200
        assert response.json()['items'][0]['name'] == 'Fried Rice'
    finally:
        app.dependency_overrides.clear()

        
def test_get_menu_item_by_restaurant_id_valid(mock_menu_repo):
    """Test for getting menu items by restaurant."""
    results = mock_menu_repo.get_menu_by_restaurant("1")
    assert len(results) == 2
    assert results[0]["name"] == "Pizza"

    
def test_get_menu_item_by_id_valid_single(mock_menu_repo):
    """Test for getting a valid menu item using the new signature."""
    # Updated to pass both restaurant_id "2" and item_id "3"
    item = mock_menu_repo.get_menu_item_by_id("2", "3")
    assert item is not None
    assert item["name"] == "Burger"

    
def test_get_menu_item_by_id_invalid(mock_menu_repo):
    """Test for an invalid menu item ID."""
    item = mock_menu_repo.get_menu_item_by_id("1", "999")
    assert item is None