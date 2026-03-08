"""Tests for restaurant_repository"""

import pytest
from app.storage.repositories.restaurant_repository import RestaurantRepository

@pytest.fixture
def mock_restaurant_repo():
    """Mock RestaurantRepository for testing."""
    repo = RestaurantRepository()

    #define a mock dataset
    mock_data = [
        {"id": "1", "name": "Restaurant 1"},
        {"id": "2", "name": "Restaurant 2"},
        {"id": "3", "name": "Restaurant 3"},
    ]

    #make the repo use this dataset
    repo.get_all = mock_data
    return repo

def test_get_restaurant_by_id_valid(mock_restaurant_repo):
    """Test for getting a valid restaurant"""
    restaurant = mock_restaurant_repo.get_restaurant_by_id("1")

    assert restaurant is not None
    assert restaurant["id"] == "1"
    assert restaurant["name"] == "Restaurant 1"

def test_get_restaurant_by_id_invalid(mock_restaurant_repo):
    """Test for trying to get an invalid restaurant"""
    restaurant = mock_restaurant_repo.get_restaurant_by_id("999")

    assert restaurant is None

