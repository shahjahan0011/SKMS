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