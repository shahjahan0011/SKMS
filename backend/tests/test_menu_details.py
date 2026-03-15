""" Test Menu_details retrieval"""

import pytest

from app.storage.repositories.menu_repository import MenuRepository

@pytest.fixture
def repo():
    return MenuRepository()

def test_get_menu_item_detail_success(client):
    """
    Test FR6: Successful retrieval of detailed menu item.
    """
    restaurant_id = "1"
    item_id = "1"

    response = client.get(f"/menus/{restaurant_id}/items/{item_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["item_name"] == "Beef pie"


def test_fr6_get_menu_item_by_id_valid(repo):
    """ Pass both IDs: restaurant_id "1" and item_id "1" """
    result = repo.get_menu_item_by_id("1", "1")
    assert result is not None
    assert result["item_name"] == "Beef pie"


def test_fr6_get_menu_item_by_id_invalid(repo):
    """ Use an item_id that doesn't exist for restaurant "1"""
    result = repo.get_menu_item_by_id("1", "999")
    assert result is None
