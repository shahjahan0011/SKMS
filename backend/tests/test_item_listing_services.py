"""Tests for item_listing_services"""

from app.services.item_listing_services import item_listing_service

# test repositories to test the service layer for item listing
class test_restaurant_repo:
    """Test restaurant repository for testing purposes"""

    def get_all_restaurants(self):
        return [
            {"id": "1", "name": "Restaurant 1"},
            {"id": "2", "name": "Restaurant 2"}
        ]
    def get_restaurant_by_id(self, restaurant_id):
        for r in self.get_all_restaurants():
            if r["id"] == restaurant_id:
                return r
        return None

class test_menu_repo:
    """Test menu repository for testing purposes"""

    def get_menu_by_restaurant(self, restaurant_id):
        return [
            {
                "id": "1",
                "restaurant_id": restaurant_id,
                "item_name": "Burger",
                "price": "10"
            }
        ]

    def get_menu_item_by_id(self, item_id):
        if item_id == "1":
            return {"id": "1", "restaurant_id": "1", "item_name": "Burger", "price": "10"}
        return None

# pytests for item listing services
def test_get_all_restaurants():
    """Test for Get All Restaurants"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    restaurants = service.get_all_restaurants()

    assert len(restaurants) == 2

def test_get_restaurant_menu_valid():
    """Test for Get Restaurant Menu - Valid Restaurant"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    menu = service.get_restaurant_menu("1")

    assert len(menu) == 1
    assert menu[0]["item_name"] == "Burger"


def test_get_restaurant_menu_invalid():
    """Test case for Get Restaurant Menu - Invalid Restaurant"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    try:
        service.get_restaurant_menu("999")
        assert False
    except ValueError:
        assert True

def test_get_restaurant_by_id_valid():
    """Test for Get a valid restaurant by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    restaurant = service.get_restaurant_by_id("1")

    assert restaurant["id"] == "1"


def test_get_restaurant_by_id_invalid():
    """Test for Get an invalid restaurant by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    try:
        service.get_restaurant_by_id("999")
        assert False
    except ValueError:
        assert True


def test_get_menu_item_by_id_valid():
    """Test for Get a valid menu item by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    item = service.get_menu_item_by_id("1")

    assert item["id"] == "1"


def test_get_menu_item_by_id_invalid():
    """Test for Get an invalid menu item by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    try:
        service.get_menu_item_by_id("999")
        assert False
    except ValueError:
        assert True

def get_restaurant_menu(self, restaurant_id: str) -> list:
    """Get menu items for a given restaurant"""
    restaurants = self.restaurant_repo.get_all_restaurants()

    exists = any(r["id"] == restaurant_id for r in restaurants)

    if not exists:
        raise ValueError("Restaurant not found")

    menu_items = self.menu_repo.get_menu_by_restaurant(restaurant_id)
    restaurant_ids = {r["id"] for r in restaurants}

    for item in menu_items:
        if item["restaurant_id"] not in restaurant_ids:
            raise ValueError("Menu item references invalid restaurant")

    return menu_items
