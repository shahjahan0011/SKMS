"""Tests for item_listing_services"""

from app.services.item_listing_services import item_listing_service


class test_restaurant_repo:
    """temporary restaurant repository for testing purposes"""

    def get_all_restaurants(self):
        """test for getting all restaurants"""
        return [
            {"id": "1", "name": "Restaurant 1"},
            {"id": "2", "name": "Restaurant 2"}
        ]
    def get_restaurant_by_id(self, restaurant_id):
        """test for getting restaurant by id"""
        for r in self.get_all_restaurants():
            if r["id"] == restaurant_id:
                return r
        return None

class test_menu_repo:
    """temporary menu repository for testing purposes"""

    def get_menu_by_restaurant(self, restaurant_id):
        """test for getting menu by restaurant id"""
        return [
            {
                "id": "1",
                "restaurant_id": restaurant_id,
                "item_name": "Burger",
                "price": "10"
            }
        ]


    def get_menu_item_by_id(self, item_id):
        """test for getting menu item by id"""
        if item_id == "1":
            return {"id": "1", "restaurant_id": "1", "item_name": "Burger", "price": "10"}
        return None



def test_get_all_restaurants():
    """test for getting all restaurants"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    restaurants = service.get_all_restaurants()

    assert len(restaurants) == 2



def test_get_restaurant_menu_valid():
    """test for getting menu for a valid restaurant"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    menu = service.get_restaurant_menu("1")

    assert len(menu) == 1
    assert menu[0]["item_name"] == "Burger"



def test_get_restaurant_menu_invalid():
    """test for getting menu for an invalid restaurant"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    error_raised = False
    try:
        service.get_restaurant_menu("999")
    except ValueError:
        error_raised = True
    
    assert error_raised



def test_get_restaurant_by_id_valid():
    """test for getting valid restaurant by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    restaurant = service.get_restaurant_by_id("1")

    assert restaurant["id"] == "1"



def test_get_restaurant_by_id_invalid():
    """test for getting invalid restaurant by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    error_raised = False
    try:
        service.get_restaurant_menu("999")
    except ValueError:
        error_raised = True
    
    assert error_raised



def test_get_menu_item_by_id_valid():
    """test for getting a valid menu item by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    item = service.get_menu_item_by_id("1")

    assert item["id"] == "1"



def test_get_menu_item_by_id_invalid():
    """test for getting an invalid menu item by id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    error_raised = False
    try:
        service.get_restaurant_menu("999")
    except ValueError:
        error_raised = True
    
    assert error_raised



def get_restaurant_menu(self, restaurant_id: str) -> list:
    """test for getting menu items for a given restaurant"""
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
