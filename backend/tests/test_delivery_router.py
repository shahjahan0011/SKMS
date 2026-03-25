"""Tests for Delivery Router"""

from fastapi.testclient import TestClient
from app.main import app
from app.routers.delivery_router import delivery_service

client = TestClient(app)


def setup_router_env(tmp_path):
    delivery_service.repo.file_path = tmp_path / "deliveries.csv"
    delivery_service.repo.agent_file = tmp_path / "agents.csv"
    delivery_service.repo.location_file = tmp_path / "locations.csv"

    with open(delivery_service.repo.file_path, mode = "w") as file:
        file.write("order_id,restaurant_id,user_id,user_name,unit,street,postal_code,province,city,country,status,is_emergency,agent_id,agent_name\n")

    with open(delivery_service.repo.agent_file, mode = "w") as file:
        file.write("agent_id,name,is_available\n")
        file.write("1,agent1,True\n")

    with open(delivery_service.repo.location_file, mode = "w") as file:
        file.write("location_id,user_id,name,unit,street,postal_code,province,city,country\n")



location = type("Location", (), {
    "unit": 123,
    "street": "University Way",
    "postal_code": "V1V1V7",
    "province": "British Columbia",
    "city": "Kelowna",
    "country": "Canada"
})()



def create_test_delivery(order_id, user_id=1, user_name="khushi"):
    """general method for creating delivery"""
    
    return {
        "order_id": order_id,
        "restaurant_id": 1,
        "user_id": user_id,
        "user_name": user_name,
        "delivery_location": location,
        "status": "preparing",
        "is_emergency": False
    }



def create_test_location(location_id, user_id=1, name="home"):
    """general method for creating location"""
    
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
    """test for getting all deliveries"""

    setup_router_env(tmp_path)
    delivery_service.repo.create_delivery(create_test_delivery(1, 2, "khushi"))
    response = client.get("/deliveries")

    assert response.status_code == 200
    assert len(response.json()) == 1



def test_get_delivery_by_order_id(tmp_path):
    """test for getting delivery by order id"""

    setup_router_env(tmp_path)
    delivery_service.repo.create_delivery(create_test_delivery(2, 1, "khushi"))
    response = client.get("/deliveries/2")

    assert response.status_code == 200
    assert response.json()["order_id"] == "2"



def test_create_delivery(tmp_path):
    """test for creating delivery from router"""

    setup_router_env(tmp_path)
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
    """test for updating delivery status from router"""

    setup_router_env(tmp_path)
    delivery_service.repo.create_delivery(create_test_delivery(4, 6, "khushi"))
    response = client.patch(
        "/deliveries/4/status",
        json={"new_status": "on the way"}
    )

    assert response.status_code == 200

    delivery = delivery_service.repo.get_delivery_by_order_id(4)
    assert delivery["status"] == "on the way"



def test_get_user_deliveries(tmp_path):
    """test for getting deliveries for user"""

    setup_router_env(tmp_path)
    delivery_service.repo.create_delivery(create_test_delivery(5, 10, "khushi01"))
    delivery_service.repo.create_delivery(create_test_delivery(6, 11, "khushi02"))
    response = client.get("/deliveries/user/10")

    assert response.status_code == 200
    assert response.json()[0]["order_id"] == "5"



def test_save_location(tmp_path):
    """test for saving location"""

    setup_router_env(tmp_path)
    response = client.post(
        "/locations?user_id=5&name=home",
        json={
            "unit": 123,
            "street": "University Way",
            "postal_code": "V1V1V7",
            "province": "British Columbia",
            "city": "Kelowna",
            "country": "Canada"
        }
    )

    assert response.status_code == 200

    locations = delivery_service.repo.get_all_locations()
    assert locations[0]["user_id"] == "5"



def test_get_user_locations(tmp_path):
    """test for getting locations for a user"""

    setup_router_env(tmp_path)
    delivery_service.repo.save_location(create_test_location(1, 5, "home"))
    response = client.get("/locations/user/5")

    assert response.status_code == 200
    assert response.json()[0]["user_id"] == "5"



def test_delete_location(tmp_path):
    """test for deleting location"""

    setup_router_env(tmp_path)
    delivery_service.repo.save_location(create_test_location(1, 3, "home"))
    response = client.delete("/locations/1")
    assert response.status_code == 200

    locations = delivery_service.repo.get_all_locations()
    assert locations == []



def test_get_all_locations(tmp_path):
    """test for getting all locations"""

    setup_router_env(tmp_path)
    delivery_service.repo.save_location(create_test_location(1, 1, "home"))
    response = client.get("/locations")

    assert response.status_code == 200
    assert len(response.json()) == 1



def test_get_available_agent(tmp_path):
    """test for getting available agents"""

    setup_router_env(tmp_path)
    response = client.get("/agents/available")

    assert response.status_code == 200
    assert response.json()["agent_id"] == "1"



def test_get_delivery_invalid_id(tmp_path):
    """test for getting delivery with invalid id"""

    setup_router_env(tmp_path)
    response = client.get("/deliveries/999")

    assert response.status_code == 404



def test_create_delivery_invalid_status(tmp_path):
    """test for creating delivery with invalid status"""

    setup_router_env(tmp_path)
    response = client.post(
        "/deliveries",
        json={
            "order_id": 10,
            "restaurant_id": 1,
            "user_id": 1,
            "user_name": "test",
            "delivery_location": {
                "unit": 1,
                "street": "test",
                "postal_code": "123",
                "province": "BC",
                "city": "Kelowna",
                "country": "Canada"
            },
            "status": "INVALID",
            "is_emergency": False
        }
    )

    assert response.status_code == 400



def test_create_delivery_no_agents(tmp_path):
    """test for create delivery when no agents available"""

    setup_router_env(tmp_path)
    with open(delivery_service.repo.agent_file, "w") as file:
        file.write("agent_id,name,is_available\n")
        file.write("1,agent1,False\n")

    response = client.post(
        "/deliveries",
        json={
            "order_id": 20,
            "restaurant_id": 1,
            "user_id": 1,
            "user_name": "test",
            "delivery_location": {
                "unit": 1,
                "street": "test",
                "postal_code": "123",
                "province": "BC",
                "city": "Kelowna",
                "country": "Canada"
            },
            "status": "placed",
            "is_emergency": False
        }
    )

    assert response.status_code == 400



def test_delete_location_invalid(tmp_path):
    """test for deleting non-existent location"""

    setup_router_env(tmp_path)
    response = client.delete("/locations/999")

    assert response.status_code == 400