"""Tests for restaurant_repository"""

from app.storage.repositories.restaurant_repository import RestaurantRepository


def test_get_restaurant_by_id_valid():
    """Test for get a valid restaurant"""
    repo = RestaurantRepository()

    restaurant = repo.get_restaurant_by_id("16")

    assert restaurant is not None
    assert restaurant["id"] == "16"


def test_get_restaurant_by_id_invalid():
    """Test for get an invalid restaurant"""
    repo = RestaurantRepository()

    restaurant = repo.get_restaurant_by_id("9999")

    assert restaurant is None