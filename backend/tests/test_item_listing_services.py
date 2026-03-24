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


class faulty_restaurant_repo:
    """test for wrong restaurant"""
    def get_all_restaurants(self):
        raise Exception("Database Failure")
    


def test_get_all_restaurants():
    """test for getting all restaurants"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    restaurants = service.get_all_restaurants()

    assert len(restaurants) == 2
    assert restaurants[0]["id"] == "1"



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
    error_message = ""

    try:
        service.get_restaurant_menu("999")
    except ValueError as e:
        error_raised = True
        error_message = str(e)

    assert error_raised
    assert error_message == "Invalid Restaurant"



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
        service.get_restaurant_by_id("999")
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
        service.get_menu_item_by_id("999")
    except ValueError:
        error_raised = True
    
    assert error_raised



def test_get_restaurant_menu_empty_id():
    """test for empty restaurant id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    error_raised = False

    try:
        service.get_restaurant_menu("")
    except ValueError:
        error_raised = True

    assert error_raised



def test_get_menu_item_by_id_empty():
    """test for empty menu item id"""
    service = item_listing_service(test_restaurant_repo(), test_menu_repo())

    error_raised = False

    try:
        service.get_menu_item_by_id("")
    except ValueError:
        error_raised = True

    assert error_raised



def test_get_restaurant_menu_repo_failure():
    """test when repository fails"""
    service = item_listing_service(faulty_restaurant_repo(), test_menu_repo())

    error_raised = False

    try:
        service.get_restaurant_menu("1")
    except Exception:
        error_raised = True

    assert error_raised