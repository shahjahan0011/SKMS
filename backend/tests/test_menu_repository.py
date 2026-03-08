"""Tests for MenuRepository."""

from app.storage.repositories.menu_repository import MenuRepository


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