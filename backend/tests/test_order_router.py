from fastapi.testclient import TestClient
from app.main import app
from app.routers import order_router

client = TestClient(app)


def test_create_order_route(monkeypatch):
    def mock_create_order(username, items, is_premium=False):
        return {
            "order_id": "o1",
            "username": username,
            "restaurant_id": "rest_1",
            "is_premium": "true" if is_premium else "false",
            "base_cost": "20.00",
            "tax": "1.00",
            "delivery_fee": "4.99",
            "total": "25.99",
            "status": "pending",
        }

    monkeypatch.setattr(order_router, "create_order", mock_create_order)

    response = client.post(
        "/orders/",
        json={
            "username": "jahan",
            "items": [
                {"id": "item_1", "quantity": 2},
            ],
            "is_premium": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "jahan"
    assert data["restaurant_id"] == "rest_1"
    assert data["status"] == "pending"
    assert data["is_premium"] == "false"

def test_get_order_route(monkeypatch):
    def mock_get_order_status(order_id):
        return {"order_id": order_id, "status": "pending"}

    monkeypatch.setattr(order_router, "get_order_by_id", mock_get_order_status)

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

def test_get_order_history_route(monkeypatch):
    """Test order history endpoint"""
    
    def mock_get_order_history(username):
        return [
            {
                "order_id": "o1",
                "username": username,
                "restaurant_id": "rest_1",
                "is_premium": "true",
                "base_cost": "35.00",
                "tax": "1.75",
                "delivery_fee": "0.00",
                "total": "36.75",
                "status": "delivered",
                "created_at": "2026-03-24T12:00:00",
                "items": [
                    {"order_item_id": "oi1", "item_id": "item_1", "quantity": "2", "item_price": "10.00"},
                ],
            }
        ]
    
    monkeypatch.setattr(order_router, "get_order_history", mock_get_order_history)
    
    response = client.get("/orders/jahan/history")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["username"] == "jahan"
    assert data[0]["order_id"] == "o1"
    assert "items" in data[0]
    assert len(data[0]["items"]) == 1

def test_create_multi_item_order_route(monkeypatch):
    def mock_create_order(username, items, is_premium=False):
        return {
            "order_id": "o1",
            "username": username,
            "restaurant_id": "rest_1",
            "is_premium": "false",
            "base_cost": "25.00",
            "tax": "1.25",
            "delivery_fee": "4.99",
            "total": "31.24",
            "status": "pending",
        }

    monkeypatch.setattr(order_router, "create_order", mock_create_order)

    response = client.post(
        "/orders/",
        json={
            "username": "jahan",
            "items": [
                {"id": "item_1", "quantity": 1},
                {"id": "item_2", "quantity": 1},
            ],
            "is_premium": False,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "jahan"
    assert data["status"] == "pending"