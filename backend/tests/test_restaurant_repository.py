"""Tests for restaurant_repository"""

from app.storage.repositories.restaurant_repository import RestaurantRepository
from app.storage.csv_store import CSVStore

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

def test_invalid_restaurant_data():
    """Test validation for invalid restaurant dataset"""

    original_read_csv = CSVStore.read_csv

    def fake_read_csv(path):
        return [{"id": "", "name": "Test"}]

    CSVStore.read_csv = fake_read_csv

    repo = RestaurantRepository()

    try:
        repo.get_all_restaurants()
        assert False
    except ValueError:
        assert True

    CSVStore.read_csv = original_read_csv
    