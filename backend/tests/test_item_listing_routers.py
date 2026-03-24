"""Test for Item Listing Routers"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_get_all_restaurants():
    """test for getting restaurants endpoint"""
    response = client.get("/restaurants")
    print(f"DEBUG RESPONSE: {response.json()}")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)



def test_get_restaurant_by_id_valid():
    """test for getting a valid restaurant id"""
    response = client.get("/restaurants/1")

    assert response.status_code == 200
    assert response.json()["id"] == "1"



def test_get_restaurant_by_id_invalid():
    """test for getting an invalid restaurant id"""
    response = client.get("/restaurants/999999")

    assert response.status_code == 404



def test_get_restaurant_menu_valid():
    """test for getting a valid menu for a restaurant"""
    response = client.get("/restaurants/1/menu")

    assert response.status_code == 200
    assert isinstance(response.json().get("items", []), list)



def test_get_restaurant_menu_invalid():
    """test for getting an invalid menu for a restaurant"""
    response = client.get("/restaurants/999999/menu")

    assert response.status_code == 404



def test_get_menu_item_by_id_valid():
    """test for getting a valid menu item by id"""
    response = client.get("/menu/1")

    assert response.status_code == 200
    assert response.json()["id"] == "1"



def test_get_menu_item_by_id_invalid():
    """test for getting an invalid menu item by id"""
    response = client.get("/menu/999999")

    assert response.status_code == 404
