"""Tests for restaurant_repository"""

import pytest
from unittest.mock import MagicMock
from app.storage.repositories.restaurant_repository import restaurant_repository

@pytest.fixture
def mock_restaurant_repo():
    """Mock restaurant_repository for testing using snake_case."""
    repo = restaurant_repository()

    mock_data = [
        {"id": "1", "name": "Pasta Place", "cuisine": "Italian", "is_active": "true"},
        {"id": "2", "name": "Curry House", "cuisine": "Indian", "is_active": "true"},
        {"id": "3", "name": "Burger Joint", "cuisine": "American", "is_active": "false"},
    ]

    # Mock the get_all method to return our mock_data
    repo.get_all = MagicMock(return_value=mock_data)
    repo.get_all_restaurants = MagicMock(return_value=mock_data)
    
    return repo


def test_get_restaurant_by_id_valid(mock_restaurant_repo):
    """Test for getting a valid restaurant by ID."""
    restaurant = mock_restaurant_repo.get_restaurant_by_id("1")
    assert restaurant is not None
    assert restaurant["name"] == "Pasta Place"
    assert restaurant["id"] == "1"

def test_get_restaurant_by_id_invalid(mock_restaurant_repo):
    """Test for trying to get an invalid restaurant."""
    restaurant = mock_restaurant_repo.get_restaurant_by_id("999")
    assert restaurant is None


def test_search_restaurant_by_cuisine(mock_restaurant_repo):
    """Test searching by cuisine keyword."""
    results = mock_restaurant_repo.get_restaurants_by_search("Italian")
    assert len(results) == 1
    assert results[0]["cuisine"] == "Italian"

def test_search_restaurant_case_insensitive(mock_restaurant_repo):
    """Test search is case insensitive and works on the name."""
    # Search for 'indian' should find 'Curry House'
    results = mock_restaurant_repo.get_restaurants_by_search("indian")
    assert len(results) == 1
    assert "Curry House" in results[0]["name"]