"""Integration Tests for MenuRepository."""
import pytest
from app.storage.repositories.menu_repository import menu_repository


def test_get_menu_by_restaurant_id_from_csv():
    """
    Test that the repository can correctly fetch and parse
    data from the actual CSV storage.
    """
    repo = menu_repository()

    result = repo.get_menu_by_restaurant("13")

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

    result = repo.get_menu_by_restaurant("non_existent_id")

    assert result == []


def test_get_menu_item_structure():
    """
    Verify that the data returned from the CSV has
    all the required keys for the front-end.
    """
    repo = menu_repository()
    result = repo.get_menu_by_restaurant("13")

    if len(result) > 0:
        first_item = result[0]
        assert "id" in first_item
        assert "item_name" in first_item
        assert "price" in first_item
        assert "restaurant_id" in first_item

def test_deduct_inventory_logic(mock_menu_repo):
    """Test that deducting inventory updates the CSV and change availability to false"""
    item_id = "1"
    initial_stock = 10
    quantity_to_order = 10

    mock_menu_repo.update_item_inventory(item_id, initial_stock, True)

    result = mock_menu_repo.deduct_inventory(item_id, quantity_to_order)

    assert result["success"] is True
    assert result["new_stock"] == 0
    assert result["sold_out_just_now"] is True

    updated_item = mock_menu_repo.get_menu_item_by_id(item_id)
    assert int(updated_item["stock_count"]) == 0
    assert str(updated_item["is_available"]) == "False"
