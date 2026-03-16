"""Tests for Delivery Service"""

from app.services.delivery_services import delivery_services

location = type("Location", (), {
    "unit": 123,
    "street": "University Way",
    "postal_code": "V1V1V7",
    "province": "British Columbia",
    "city": "Kelowna",
    "country": "Canada"
})()

def test_get_all_deliveries(tmp_path):
    """test getting all deliveries"""

    service = delivery_services()
    service.repo.file_path = tmp_path / "deliveries.csv"

    with open(service.repo.file_path, "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    service.repo.create_delivery({
        "order_id": 1,
        "restaurant_id": 5,
        "user_id": 2,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    deliveries = service.get_all_deliveries()

    assert len(deliveries) == 1


def test_get_delivery_by_order_id(tmp_path):
    """test getting delivery by order id"""

    service = delivery_services()

    service.repo.file_path = tmp_path / "deliveries.csv"

    with open(service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    service.repo.create_delivery({
        "order_id": 1,
        "restaurant_id": 3,
        "user_id": 1,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    result = service.get_delivery_by_order_id(1)

    assert result["order_id"] == "1"


def test_create_delivery(tmp_path):
    """test creating a delivery"""
    service = delivery_services()

    service.repo.file_path = tmp_path / "deliveries.csv"

    with open(service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    service.create_delivery(
        3,
        1,
        5,
        "khushi",
        location,
        "preparing",
        False
    )

    delivery = service.repo.get_delivery_by_order_id(3)

    assert delivery["order_id"] == "3"
    assert delivery["user_name"] == "khushi"


def test_update_delivery_status(tmp_path):
    """test updating delivery status"""

    service = delivery_services()

    service.repo.file_path = tmp_path / "deliveries.csv"

    with open(service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    service.repo.create_delivery({
        "order_id": 4,
        "restaurant_id": 2,
        "user_id": 6,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    service.update_delivery_status(4, "on the way")
    delivery = service.repo.get_delivery_by_order_id(4)

    assert delivery["status"] == "on the way"


def test_get_user_deliveries(tmp_path):
    """test getting deliveries for a user"""

    service = delivery_services()
    service.repo.file_path = tmp_path / "deliveries.csv"

    with open(service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    service.repo.create_delivery({
        "order_id": 5,
        "restaurant_id": 3,
        "user_id": 10,
        "user_name": "khushi 01",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    service.repo.create_delivery({
        "order_id": 6,
        "restaurant_id": 4,
        "user_id": 11,
        "user_name": "khushi 02",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    deliveries = service.get_user_deliveries(10)
    assert deliveries[0]["order_id"] == "5"
    assert deliveries[0]["user_id"] == "10"