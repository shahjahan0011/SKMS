"""Tests for MenuRepository."""

import pytest
from unittest.mock import MagicMock
from app.storage.repositories.menu_repository import MenuRepository

@pytest.fixture
def mock_menu_repo():
    """Mock MenuRepository for testing."""
    repo = MenuRepository()

    #define a mock dataset
    mock_data = [
        {"id": "1", "restaurant_id": "1", "name": "Pizza", "price": "10"},
        {"id": "2", "restaurant_id": "1", "name": "Pasta", "price": "12"},
        {"id": "3", "restaurant_id": "2", "name": "Burger", "price": "8"},
    ]

    #make the repo use this dataset
    repo.get_all = MagicMock(return_value=mock_data)

    #define get_menu_by_restaurant to filter the mock data by restaurant_id
    def get_item_by_id(item_id):
        # only return an item if the id matches the mock data, otherwise return None
        for item in mock_data():
            if item["id"] == item_id:
                return item
        return None

    repo.get_menu_by_restaurant = MagicMock(side_effect = get_item_by_id)

    repo.get_menu_by_restaurant = MagicMock(return_value=[mock_data[0], mock_data[1]])

    return repo

def test_get_menu_item_by_restaurant_id_valid(mock_menu_repo):
    """Test for getting a valid menu item"""
    results = mock_menu_repo.get_menu_by_restaurant("2")

    assert len(results) == 2
    assert results[0]["id"] == "1"
    assert results[0]["name"] == "Pizza"

def test_get_menu_item_by_id_valid_single(mock_menu_repo):
    """Test for getting a valid menu item by ID"""
    item = mock_menu_repo.get_menu_item_by_id("3")

    assert item is not None
    assert item["id"] == "3"
    assert item["name"] == "Burger"

def test_get_menu_item_by_id_invalid(mock_menu_repo):
    """Test for trying to get an invalid menu item by ID"""
    item = mock_menu_repo.get_menu_item_by_id("999")

    assert item is None

