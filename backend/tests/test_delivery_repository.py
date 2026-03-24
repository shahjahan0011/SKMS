"""Tests for Delivery Repository"""

import csv
from app.storage.repositories.delivery_repository import delivery_repository


def test_get_all_deliveries():
    """get a list of deliveries"""

    repo = delivery_repository()

    deliveries = repo.get_all_deliveries()

    assert deliveries != None


def test_get_delivery_by_order_id():
    """get by order id"""

    repo = delivery_repository()

    result = repo.get_delivery_by_order_id(1)

    if result:
        assert result["order_id"] == "1"


def test_create_delivery(tmp_path):
    """test to check if a new delivery is created"""
    repo = delivery_repository()

    repo.file_path = tmp_path / "deliveries.csv"

    with open(repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    repo.create_delivery({
        "order_id": 10,
        "restaurant_id": 3,
        "user_id": 1,
        "user_name": "test_user",
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
    })

    deliveries = repo.get_all_deliveries()

    assert deliveries[-1]["order_id"] == "10"


def test_update_delivery_status(tmp_path):
    """check updating delivery status"""

    repo = delivery_repository()

    repo.file_path = tmp_path / "deliveries.csv"

    with open(repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    repo.create_delivery({
        "order_id": 10,
        "restaurant_id": 3,
        "user_id": 1,
        "user_name": "test_user",
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
    })

    repo.update_delivery_status(10, "on the way")
    delivery = repo.get_delivery_by_order_id(10)
    
    assert delivery["status"] == "on the way"


def test_get_user_deliveries(tmp_path):
    """check retrieving deliveries for a specific user"""

    repo = delivery_repository()
    repo.file_path = tmp_path / "deliveries.csv"

    with open(repo.file_path, "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    repo.create_delivery({
        "order_id": 1,
        "restaurant_id": 5,
        "user_id": 2,
        "user_name": "khushi01",
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
    })

    repo.create_delivery({
        "order_id": 2,
        "restaurant_id": 3,
        "user_id": 1,
        "user_name": "khushi02",
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
    })

    deliveries = repo.get_user_deliveries(2)
    assert deliveries[0]["order_id"] == "1"
    assert deliveries[0]["user_id"] == "2"


def test_save_location(tmp_path):
    """test to see saving a location"""

    repo = delivery_repository()

    repo.location_file = tmp_path / "locations.csv"

    with open(repo.location_file, "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")

    repo.save_location({
        "location_id": 1,
        "user_id": 5,
        "name": "home",
        "unit": 123,
        "street": "University Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    locations = repo.get_all_locations()

    assert locations[0]["location_id"] == "1"
    assert locations[0]["user_id"] == "5"


def test_get_user_locations(tmp_path):
    """test for getting locations for a user"""

    repo = delivery_repository()

    repo.location_file = tmp_path / "locations.csv"

    with open(repo.location_file, "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")

    repo.save_location({
        "location_id": 1,
        "user_id": 2,
        "name": "home",
        "unit": 123,
        "street": "University Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    repo.save_location({
        "location_id": 2,
        "user_id": 1,
        "name": "work",
        "unit": 456,
        "street": "Academy Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    locations = repo.get_user_locations(2)

    assert locations[0]["user_id"] == "2"
    assert locations[0]["location_id"] == "1"


def test_delete_location(tmp_path):
    """test for deleting a location"""

    repo = delivery_repository()

    repo.location_file = tmp_path / "locations.csv"

    with open(repo.location_file, "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")

    repo.save_location({
        "location_id": 1,
        "user_id": 2,
        "name": "home",
        "unit": 123,
        "street": "University Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    repo.delete_location(1)

    locations = repo.get_all_locations()

    assert locations == []


def test_get_all_locations(tmp_path):
    """test for getting all locations"""

    repo = delivery_repository()

    repo.location_file = tmp_path / "locations.csv"

    with open(repo.location_file, "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")

    repo.save_location({
        "location_id": 1,
        "user_id": 2,
        "name": "home",
        "unit": 123,
        "street": "University Way",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    repo.save_location({
        "location_id": 2,
        "user_id": 3,
        "name": "work",
        "unit": 456,
        "street": "Lakeshore",
        "postal_code": "V1V1V7",
        "province": "British Columbia",
        "city": "Kelowna",
        "country": "Canada"
    })

    locations = repo.get_all_locations()

    assert len(locations) == 2


def test_get_available_agent(tmp_path):
    repo = delivery_repository()

    repo.agent_file = tmp_path / "agents.csv"

    with open(repo.agent_file, "w") as file:
        file.write("agent_id,name,is_available\n")
        file.write("1,agent1,\n")
        file.write("2,agent2,True\n")

    agent = repo.get_available_agent()

    assert agent["agent_id"] == "2"


def test_set_agent_busy(tmp_path):
    repo = delivery_repository()

    repo.agent_file = tmp_path / "agents.csv"

    with open(repo.agent_file, "w") as file:
        file.write("agent_id,name,is_available\n")
        file.write("1,agent1,True\n")

    repo.set_agent_busy(1)

    agent = repo.get_available_agent()

    assert agent is None


def test_get_available_agent_none(tmp_path):
    repo = delivery_repository()

    repo.agent_file = tmp_path / "agents.csv"

    with open(repo.agent_file, "w") as file:
        file.write("agent_id,name,is_available\n")
        file.write("1,agent1,False\n")

    agent = repo.get_available_agent()

    assert agent is None
