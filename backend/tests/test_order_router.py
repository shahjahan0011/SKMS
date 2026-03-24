from fastapi.testclient import TestClient
from app.main import app
from app.routers import order_router

client = TestClient(app)


def test_create_order_route(monkeypatch):
    def mock_create_order(username, id, quantity, is_premium):
        return {
            "order_id": "o1",
            "username": username,
            "id": id,
            "quantity": str(quantity),
            "status": "pending",
        }

    monkeypatch.setattr(order_router, "create_order", mock_create_order)

    response = client.post(
        "/orders/",
        json={
            "username": "jahan",
            "id": "item_1",
            "quantity": 2,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "jahan"
    assert data["id"] == "item_1"
    assert data["status"] == "pending"


def test_get_order_route(monkeypatch):
    def mock_get_order_status(order_id):
        return {"order_id": order_id, "status": "pending"}

    monkeypatch.setattr(order_router, "get_order_status", mock_get_order_status)

    response = client.get("/orders/o1")

    assert response.status_code == 200
    assert response.json()["order_id"] == "o1"
    assert response.json()["status"] == "pending"


def test_patch_order_status_route(monkeypatch):
    def mock_update_order_status(order_id, new_status):
        return {"order_id": order_id, "status": new_status}

    monkeypatch.setattr(order_router, "update_order_status", mock_update_order_status)

    response = client.patch(
        "/orders/o1/status",
        json={"status": "preparing"},
    )

    assert response.status_code == 200
    assert response.json()["order_id"] == "o1"
    assert response.json()["status"] == "preparing"


def test_patch_cancel_order_route(monkeypatch):
    def mock_cancel_order(order_id):
        return {"order_id": order_id, "status": "cancelled"}

    monkeypatch.setattr(order_router, "cancel_order", mock_cancel_order)

    response = client.patch("/orders/o1/cancel")

    assert response.status_code == 200
    assert response.json()["order_id"] == "o1"
    assert response.json()["status"] == "cancelled"


def test_get_active_orders_for_restaurant_route(monkeypatch):
    def mock_list_active_orders(restaurant_id):
        return [
            {"order_id": "o1", "restaurant_id": restaurant_id, "status": "pending"},
            {"order_id": "o2", "restaurant_id": restaurant_id, "status": "preparing"},
        ]

    monkeypatch.setattr(order_router, "list_active_orders", mock_list_active_orders)

    response = client.get("/orders/restaurant/rest_1/active")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["restaurant_id"] == "rest_1"