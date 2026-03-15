"""Tests for Delivery Router"""

from fastapi.testclient import TestClient
from app.main import app
from app.routers.delivery_router import delivery_service

client = TestClient(app)

# location object
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

    delivery_service.repo.file_path = tmp_path / "deliveries.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    delivery_service.repo.create_delivery({
        "order_id": 1,
        "restaurant_id": 5,
        "user_id": 2,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    response = client.get("/deliveries")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_delivery_by_order_id(tmp_path):
    """test getting delivery by order id"""

    delivery_service.repo.file_path = tmp_path / "deliveries.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    delivery_service.repo.create_delivery({
        "order_id": 2,
        "restaurant_id": 3,
        "user_id": 1,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    response = client.get("/deliveries/2")

    assert response.status_code == 200
    assert response.json()["order_id"] == "2"


def test_create_delivery(tmp_path):
    """test creating delivery from router"""

    delivery_service.repo.file_path = tmp_path / "deliveries.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    response = client.post(
        "/deliveries",
        json={
            "order_id": 3,
            "restaurant_id": 1,
            "user_id": 5,
            "user_name": "khushi",
            "delivery_location": {
                "unit": 123,
                "street": "University Way",
                "postal_code": "V1V1V7",
                "province": "British Columbia",
                "city": "Kelowna",
                "country": "Canada"
            },
            "status": "preparing",
            "is_emergency": False
        }
    )

    assert response.status_code == 200

    delivery = delivery_service.repo.get_delivery_by_order_id(3)
    assert delivery["user_name"] == "khushi"


def test_update_delivery_status(tmp_path):
    """test updating delivery status from router"""

    delivery_service.repo.file_path = tmp_path / "deliveries.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    delivery_service.repo.create_delivery({
        "order_id": 4,
        "restaurant_id": 2,
        "user_id": 6,
        "user_name": "khushi",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    response = client.patch(
        "/deliveries/4/status",
        json={"new_status": "on the way"}
    )

    assert response.status_code == 200

    delivery = delivery_service.repo.get_delivery_by_order_id(4)
    assert delivery["status"] == "on the way"


def test_get_user_deliveries(tmp_path):
    """test getting deliveries for user"""

    delivery_service.repo.file_path = tmp_path / "deliveries.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency\n")

    delivery_service.repo.create_delivery({
        "order_id": 5,
        "restaurant_id": 3,
        "user_id": 10,
        "user_name": "khushi01",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    delivery_service.repo.create_delivery({
        "order_id": 6,
        "restaurant_id": 4,
        "user_id": 11,
        "user_name": "khushi02",
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    })

    response = client.get("/deliveries/user/10")

    assert response.status_code == 200
    assert response.json()[0]["order_id"] == "5"
