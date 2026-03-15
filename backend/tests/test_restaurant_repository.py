"""Tests for restaurant_repository"""

import pytest
from app.storage.repositories.restaurant_repository import RestaurantRepository

@pytest.fixture
def mock_restaurant_repo():
    """Mock RestaurantRepository for testing."""
    repo = RestaurantRepository()

    mock_data = [
        {"id": "1", "name": "Pasta Place", "cuisine": "Italian"},
        {"id": "2", "name": "Curry House", "cuisine": "Indian"},
        {"id": "3", "name": "Burger Joint", "cuisine": "American"},
    ]

    repo.get_all = lambda: mock_data

    repo.get_restaurant_by_id = lambda res_id: next(
        (r for r in mock_data if r["id"] == res_id), None
    )

    return repo

def test_get_restaurant_by_id_valid(mock_restaurant_repo):
    restaurant = mock_restaurant_repo.get_restaurant_by_id("1")
    assert restaurant is not None
    assert restaurant["name"] == "Pasta Place"


def test_search_restaurant_by_cuisine(mock_restaurant_repo):
    """Test searching by cuisine keyword"""

    results = mock_restaurant_repo.get_restaurants_by_search("Italian")

    assert len(results) > 0
    assert any("Italian" in res["cuisine"] for res in results)


def test_search_restaurant_case_insensitive(mock_restaurant_repo):
    """Test search is case insensitive and works on the name"""

    results = mock_restaurant_repo.get_restaurants_by_search("indian")

    assert len(results) == 1
    assert "Curry House" in results[0]["name"]
