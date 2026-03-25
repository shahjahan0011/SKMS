"""Tests for Delivery Repository"""

import csv
from app.storage.repositories.delivery_repository import delivery_repository

def setup_repo_env(tmp_path):
    repo = delivery_repository()

    repo.file_path = tmp_path / "deliveries.csv"
    repo.location_file = tmp_path / "locations.csv"

    with open(repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency,agent_id,agent_name\n")

    with open(repo.location_file, mode = "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")

    return repo



def create_test_delivery(order_id, user_id=1, user_name="test_user"):
    return {
        "order_id": order_id,
        "restaurant_id": 1,
        "user_id": user_id,
        "user_name": user_name,
        "delivery_location": type("Location", (), {
            "unit": 123,
            "street": "University Way",
            "postal_code": "V1V1V7",
            "province": "British Columbia",
            "city": "Kelowna",
            "country": "Canada"
        })(),
        "status": "preparing",
        "is_emergency": False
    }



def create_test_location(location_id, user_id=1, name="home"):
    return {
        "location_id": location_id,
        "user_id": user_id,
        "name": name,
        "unit": 123,
        "street": "University Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    }



def test_get_all_deliveries(tmp_path):
    """test for getting a list of deliveries"""

    repo = setup_repo_env(tmp_path)

    repo.create_delivery(create_test_delivery(1))

    deliveries = repo.get_all_deliveries()

    assert len(deliveries) == 1



def test_get_delivery_by_order_id(tmp_path):
    """test to get by order id"""

    repo = setup_repo_env(tmp_path)

    repo.create_delivery(create_test_delivery(1))

    result = repo.get_delivery_by_order_id(1)

    assert result["order_id"] == "1"



def test_create_delivery(tmp_path):
    """test for creating a new delivery"""
    
    repo = setup_repo_env(tmp_path)
    repo.create_delivery(create_test_delivery(10))
    deliveries = repo.get_all_deliveries()

    assert deliveries[-1]["order_id"] == "10"



def test_update_delivery_status(tmp_path):
    """test for updating delivery status"""

    repo = setup_repo_env(tmp_path)
    repo.create_delivery(create_test_delivery(10))
    repo.update_delivery_status(10, "on the way")
    delivery = repo.get_delivery_by_order_id(10)
    
    assert delivery["status"] == "on the way"



def test_get_user_deliveries(tmp_path):
    """test for retrieving deliveries for a specific user"""

    repo = setup_repo_env(tmp_path)
    repo.create_delivery(create_test_delivery(1, 2, "khushi01"))
    repo.create_delivery(create_test_delivery(2, 1, "khushi02"))
    deliveries = repo.get_user_deliveries(2)

    assert deliveries[0]["order_id"] == "1"
    assert deliveries[0]["user_id"] == "2"



def test_save_location(tmp_path):
    """test for saving a location"""

    repo = setup_repo_env(tmp_path)
    repo.save_location(create_test_location(1, 5, "home"))
    locations = repo.get_all_locations()

    assert locations[0]["location_id"] == "1"
    assert locations[0]["user_id"] == "5"



def test_get_user_locations(tmp_path):
    """test for getting locations for a user"""

    repo = setup_repo_env(tmp_path)
    repo.save_location(create_test_location(1, 2, "home"))
    repo.save_location(create_test_location(2, 1, "work"))
    locations = repo.get_user_locations(2)

    assert locations[0]["user_id"] == "2"
    assert locations[0]["location_id"] == "1"



def test_delete_location(tmp_path):
    """test for deleting a location"""

    repo = setup_repo_env(tmp_path)
    repo.save_location(create_test_location(1, 2, "home"))
    repo.delete_location(1)
    locations = repo.get_all_locations()

    assert locations == []



def test_get_all_locations(tmp_path):
    """test for getting all locations"""

    repo = setup_repo_env(tmp_path)
    repo.save_location(create_test_location(1, 2, "home"))
    repo.save_location(create_test_location(2, 3, "work"))
    locations = repo.get_all_locations()

    assert len(locations) == 2



def test_get_delivery_not_found(tmp_path):
    """test for delivery not found"""

    repo = setup_repo_env(tmp_path)
    result = repo.get_delivery_by_order_id(999)

    assert result is None



def test_delete_location_invalid(tmp_path):
    """test for deleting invalid location"""

    repo = setup_repo_env(tmp_path)
    repo.delete_location(999)
    locations = repo.get_all_locations()

    assert locations == []
