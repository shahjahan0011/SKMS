"""Tests for item_listing_services"""

from app.services.item_listing_services import ItemListingService

# test repositories to test the service layer for item listing
class TestRestaurantRepo:
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

class TestMenuRepo:
    """Test menu repository for testing purposes"""

    def get_by_restaurant(self, restaurant_id):
        return [
            {
                "id": "1",
                "restaurant_id": restaurant_id,
                "item_name": "Burger",
                "price": "10"
            }
        ]

# pytests for item listing services
def test_get_all_restaurants():
    """Test for Get All Restaurants"""
    service = ItemListingService(TestRestaurantRepo(), TestMenuRepo())

    restaurants = service.get_all_restaurants()

    assert len(restaurants) == 2

def test_get_restaurant_menu_valid():
    """Test for Get Restaurant Menu - Valid Restaurant"""
    service = ItemListingService(TestRestaurantRepo(), TestMenuRepo())

    menu = service.get_restaurant_menu("1")

    assert len(menu) == 1
    assert menu[0]["item_name"] == "Burger"


def test_get_restaurant_menu_invalid():
    """Test case for Get Restaurant Menu - Invalid Restaurant"""
    service = ItemListingService(TestRestaurantRepo(), TestMenuRepo())

    try:
        service.get_restaurant_menu("999")
        assert False
    except ValueError:
        assert True

def test_get_restaurant_by_id_valid():
    service = ItemListingService(TestRestaurantRepo(), TestMenuRepo())

    restaurant = service.get_restaurant_by_id("1")

    assert restaurant["id"] == "1"


def test_get_restaurant_by_id_invalid():
    service = ItemListingService(TestRestaurantRepo(), TestMenuRepo())

    try:
        service.get_restaurant_by_id("999")
        assert False
    except ValueError:
        assert True
        