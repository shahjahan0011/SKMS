"""Integration Tests for MenuRepository."""
import pytest
from app.storage.repositories.menu_repository import menu_repository


def test_get_menu_by_restaurant_id_from_csv():
    """
    Test that the repository can correctly fetch and parse
    data from the actual CSV storage.
    """
    repo = menu_repository()

    result = repo.get_active_menu_by_restaurant("13")

    assert isinstance(result, list)
    assert len(result) > 0

    item_names = [item["item_name"] for item in result]
    assert "Briyani rice" in item_names


def test_get_menu_item_by_invalid_id():
    """
    Test that the repository returns an empty list
    when a non-existent restaurant_id is provided.
    """
    repo = menu_repository()

    result = repo.get_active_menu_by_restaurant("non_existent_id")

    assert result == []


def test_get_menu_item_structure():
    """
    Verify that the data returned from the CSV has
    all the required keys for the front-end.
    """
    repo = menu_repository()
    result = repo.get_active_menu_by_restaurant("13")

    if len(result) > 0:
        first_item = result[0]
        assert "id" in first_item
        assert "item_name" in first_item
        assert "price" in first_item
        assert "restaurant_id" in first_item
