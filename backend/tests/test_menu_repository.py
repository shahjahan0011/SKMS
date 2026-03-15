import pytest
from unittest.mock import MagicMock
from app.main import app
from app.storage.repositories.menu_repository import MenuRepository
from app.routers.menu_routers import get_menu_service

@pytest.fixture
def mock_repo():
    repo = MenuRepository()
    data = [{"id": "3", "restaurant_id": "2", "name": "Burger"}]
    repo.get_menu_item_by_id = lambda iid: next((i for i in data if i.get('id') == iid), None)
    return repo

def test_search_endpoint(client):
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
