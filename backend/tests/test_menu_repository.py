"""Tests for MenuRepository."""

from app.storage.repositories.menu_repository import MenuRepository
from app.storage.csv_store import CSVStore

def test_get_menu_item_by_id_valid():
    """Test for getting a valid menu item"""
    repo = MenuRepository()

    item = repo.get_menu_item_by_id("1")

    assert item is not None
    assert item["id"] == "1"


def test_get_menu_item_by_id_invalid():
    """Test for trying to get an invalid menu item"""
    repo = MenuRepository()

    item = repo.get_menu_item_by_id("9999")

    assert item is None

def test_invalid_menu_data():
    """Test validation for invalid menu dataset"""

    original_read_csv = CSVStore.read_csv

    def fake_read_csv(path):
        return [{"id": "", "restaurant_id": "1", "price": "10"}]

    CSVStore.read_csv = fake_read_csv

    repo = MenuRepository()

    try:
        repo.get_by_restaurant("1")
        assert False
    except ValueError:
        assert True

    CSVStore.read_csv = original_read_csv