import pytest
from fastapi import HTTPException

from app.services import order_service


def test_create_order_success(monkeypatch):
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    def mock_save_order(order_data):
        return order_data

    def mock_calculate_total_breakdown(items, is_premium=False):
        return {
            "base_cost": 20.00,
            "tax": 1.00,
            "delivery_fee": 4.99,
            "total": 25.99,
        }

    def mock_save_order_item(order_id, item_id, quantity, item_price):
        return {
            "order_item_id": "oi1",
            "order_id": order_id,
            "item_id": item_id,
            "quantity": str(quantity),
            "item_price": f"{float(item_price):.2f}",
        }

    monkeypatch.setattr(order_service, "get_menu_item_by_id", mock_get_menu_item_by_id)
    monkeypatch.setattr(order_service, "save_order", mock_save_order)
    monkeypatch.setattr(order_service, "calculate_total_breakdown", mock_calculate_total_breakdown)
    monkeypatch.setattr(order_service, "save_order_item", mock_save_order_item)

    result = order_service.create_order("jahan", "item_1", 2)

    assert result["username"] == "jahan"
    assert result["id"] == "item_1"
    assert result["restaurant_id"] == "rest_1"
    assert result["quantity"] == "2"
    assert result["price"] == "10.00"
    assert result["base_cost"] == "20.00"
    assert result["tax"] == "1.00"
    assert result["delivery_fee"] == "4.99"
    assert result["total"] == "25.99"
    assert result["status"] == "pending"
    assert result["is_premium"] == "false"


def test_create_order_premium_user(monkeypatch):
    """Test that premium users get free delivery"""
    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    def mock_save_order(order_data):
        return order_data

    def mock_calculate_total_breakdown(items, is_premium=False):
        if is_premium:
            return {
                "base_cost": 20.00,
                "tax": 1.00,
                "delivery_fee": 0.0,
                "total": 21.00,
            }
        else:
            return {
                "base_cost": 20.00,
                "tax": 1.00,
                "delivery_fee": 4.99,
                "total": 25.99,
            }

    def mock_save_order_item(order_id, item_id, quantity, item_price):
        return {
            "order_item_id": "oi1",
            "order_id": order_id,
            "item_id": item_id,
            "quantity": str(quantity),
            "item_price": f"{float(item_price):.2f}",
        }

    monkeypatch.setattr(order_service, "get_menu_item_by_id", mock_get_menu_item_by_id)
    monkeypatch.setattr(order_service, "save_order", mock_save_order)
    monkeypatch.setattr(order_service, "calculate_total_breakdown", mock_calculate_total_breakdown)
    monkeypatch.setattr(order_service, "save_order_item", mock_save_order_item)

    result = order_service.create_order("jahan", "item_1", 2, is_premium=True)

    assert result["delivery_fee"] == "0.00"
    assert result["total"] == "21.00"
    assert result["is_premium"] == "true"


def test_create_order_invalid_menu_item(monkeypatch):
    def mock_get_menu_item_by_id(item_id):
        return None

    monkeypatch.setattr(order_service, "get_menu_item_by_id", mock_get_menu_item_by_id)

    with pytest.raises(HTTPException) as exc:
        order_service.create_order("jahan", "bad_item", 1)

    assert exc.value.status_code == 404

def test_get_order_status_success(monkeypatch):
    mock_order = {"order_id": "o1", "status": "pending"}

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: mock_order)

    result = order_service.get_order_status("o1")

    assert result == mock_order


def test_get_order_status_not_found(monkeypatch):
    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: None)

    with pytest.raises(HTTPException) as exc:
        order_service.get_order_status("missing")

    assert exc.value.status_code == 404
    assert exc.value.detail == "Order not found"


def test_update_order_status_success(monkeypatch):
    order = {
        "order_id": "o1",
        "status": "pending",
        "updated_at": "",
        "delivered_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)
    monkeypatch.setattr(order_service, "update_order", lambda updated_order: updated_order)

    result = order_service.update_order_status("o1", "preparing")

    assert result["status"] == "preparing"
    assert result["updated_at"] != ""


def test_update_order_status_to_delivered_sets_delivered_at(monkeypatch):
    order = {
        "order_id": "o1",
        "status": "in-transit",
        "updated_at": "",
        "delivered_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)
    monkeypatch.setattr(order_service, "update_order", lambda updated_order: updated_order)

    result = order_service.update_order_status("o1", "delivered")

    assert result["status"] == "delivered"
    assert result["delivered_at"] != ""


def test_update_order_status_invalid_transition(monkeypatch):
    order = {
        "order_id": "o1",
        "status": "pending",
        "updated_at": "",
        "delivered_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)

    with pytest.raises(HTTPException) as exc:
        order_service.update_order_status("o1", "delivered")

    assert exc.value.status_code == 400
    assert "Invalid status transition" in exc.value.detail


def test_cancel_order_success(monkeypatch):
    order = {
        "order_id": "o1",
        "status": "pending",
        "updated_at": "",
        "cancelled_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)
    monkeypatch.setattr(order_service, "update_order", lambda updated_order: updated_order)

    result = order_service.cancel_order("o1")

    assert result["status"] == "cancelled"
    assert result["cancelled_at"] != ""
    assert result["updated_at"] != ""


def test_cancel_order_non_pending_fails(monkeypatch):
    order = {
        "order_id": "o1",
        "status": "preparing",
        "updated_at": "",
        "cancelled_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)

    with pytest.raises(HTTPException) as exc:
        order_service.cancel_order("o1")

    assert exc.value.status_code == 400
    assert exc.value.detail == "Only pending orders can be cancelled"


def test_list_active_orders(monkeypatch):
    mock_orders = [
        {"order_id": "o1", "restaurant_id": "rest_1", "status": "pending"},
        {"order_id": "o2", "restaurant_id": "rest_1", "status": "preparing"},
    ]

    monkeypatch.setattr(
        order_service,
        "get_active_orders_by_restaurant",
        lambda restaurant_id: mock_orders,
    )

    result = order_service.list_active_orders("rest_1")

    assert result == mock_orders
    assert len(result) == 2

def test_create_order_triggers_notification(monkeypatch):
    """test create order sends notification after successful save"""

    notifications = []

    class mock_notification_service:
        def notify_order_created(self, user_id, order_id):
            notifications.append((user_id, order_id))

    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    def mock_save_order(order_data):
        return order_data

    def mock_calculate_total_breakdown(items, is_premium=False):
        return {
            "base_cost": 20.00,
            "tax": 1.00,
            "delivery_fee": 4.99,
            "total": 25.99,
        }

    def mock_save_order_item(order_id, item_id, quantity, item_price):
        return {
            "order_item_id": "oi1",
            "order_id": order_id,
            "item_id": item_id,
            "quantity": str(quantity),
            "item_price": f"{float(item_price):.2f}",
        }

    monkeypatch.setattr(order_service, "get_menu_item_by_id", mock_get_menu_item_by_id)
    monkeypatch.setattr(order_service, "save_order", mock_save_order)
    monkeypatch.setattr(order_service, "calculate_total_breakdown", mock_calculate_total_breakdown)
    monkeypatch.setattr(order_service, "save_order_item", mock_save_order_item)
    monkeypatch.setattr(order_service, "NotificationService", lambda: mock_notification_service())

    result = order_service.create_order("jahan", "item_1", 2)

    assert result["username"] == "jahan"
    assert len(notifications) == 1
    assert notifications[0][0] == "jahan"
    assert notifications[0][1] == result["order_id"]


def test_update_order_status_triggers_notification(monkeypatch):
    """test status change sends notification after successful update"""

    notifications = []

    class mock_notification_service:
        def notify_order_status_changed(self, user_id, order_id, new_status):
            notifications.append((user_id, order_id, new_status))

    order = {
        "order_id": "o1",
        "username": "jahan",
        "status": "pending",
        "updated_at": "",
        "delivered_at": "",
    }

    monkeypatch.setattr(order_service, "get_order_by_id", lambda order_id: order)
    monkeypatch.setattr(order_service, "update_order", lambda updated_order: updated_order)
    monkeypatch.setattr(order_service, "NotificationService", lambda: mock_notification_service())

    result = order_service.update_order_status("o1", "preparing")

    assert result["status"] == "preparing"
    assert len(notifications) == 1
    assert notifications[0] == ("jahan", "o1", "preparing")


def test_create_order_still_succeeds_if_notification_fails(monkeypatch):
    """test notification failure does not break order creation"""

    class mock_notification_service:
        def notify_order_created(self, user_id, order_id):
            raise Exception("notification failed")

    def mock_get_menu_item_by_id(item_id):
        return {
            "id": item_id,
            "restaurant_id": "rest_1",
            "price": "10.00",
        }

    def mock_save_order(order_data):
        return order_data

    def mock_calculate_total_breakdown(items, is_premium=False):
        return {
            "base_cost": 20.00,
            "tax": 1.00,
            "delivery_fee": 4.99,
            "total": 25.99,
        }

    def mock_save_order_item(order_id, item_id, quantity, item_price):
        return {
            "order_item_id": "oi1",
            "order_id": order_id,
            "item_id": item_id,
            "quantity": str(quantity),
            "item_price": f"{float(item_price):.2f}",
        }

    monkeypatch.setattr(order_service, "get_menu_item_by_id", mock_get_menu_item_by_id)
    monkeypatch.setattr(order_service, "save_order", mock_save_order)
    monkeypatch.setattr(order_service, "calculate_total_breakdown", mock_calculate_total_breakdown)
    monkeypatch.setattr(order_service, "save_order_item", mock_save_order_item)
    monkeypatch.setattr(order_service, "NotificationService", lambda: mock_notification_service())

    result = order_service.create_order("jahan", "item_1", 2)

    assert result["username"] == "jahan"
    assert result["status"] == "pending"

def test_get_order_history(monkeypatch):
    """Test retrieving order history with items"""
    
    def mock_get_all_orders():
        return [
            {
                "order_id": "o1",
                "username": "jahan",
                "restaurant_id": "rest_1",
                "is_premium": "true",
                "base_cost": "35.00",
                "tax": "1.75",
                "delivery_fee": "0.00",
                "total": "36.75",
                "status": "delivered",
                "created_at": "2026-03-20T10:00:00",
            },
            {
                "order_id": "o2",
                "username": "jahan",
                "restaurant_id": "rest_1",
                "is_premium": "false",
                "base_cost": "20.00",
                "tax": "1.00",
                "delivery_fee": "4.99",
                "total": "25.99",
                "status": "pending",
                "created_at": "2026-03-24T12:00:00",  # Newer
            },
            {
                "order_id": "o3",
                "username": "other_user",
                "restaurant_id": "rest_2",
                "is_premium": "false",
                "base_cost": "15.00",
                "tax": "0.75",
                "delivery_fee": "4.99",
                "total": "20.74",
                "status": "pending",
                "created_at": "2026-03-23T10:00:00",
            },
        ]
    
    def mock_get_order_items(order_id):
        if order_id == "o1":
            return [
                {"order_item_id": "oi1", "order_id": "o1", "item_id": "item_1", "quantity": "2", "item_price": "10.00"},
                {"order_item_id": "oi2", "order_id": "o1", "item_id": "item_3", "quantity": "1", "item_price": "15.00"},
            ]
        elif order_id == "o2":
            return [
                {"order_item_id": "oi3", "order_id": "o2", "item_id": "item_1", "quantity": "2", "item_price": "10.00"},
            ]
        else:
            return []
    
    monkeypatch.setattr(order_service, "get_all_orders", mock_get_all_orders)
    monkeypatch.setattr("app.storage.repositories.order_items_repository.get_order_items", mock_get_order_items)
    
    result = order_service.get_order_history("jahan")
    
    # Should return only jahan's orders
    assert len(result) == 2
    
    # Should be sorted by created_at descending (newest first)
    assert result[0]["order_id"] == "o2"  # 2026-03-24
    assert result[1]["order_id"] == "o1"  # 2026-03-20
    
    # Should have items
    assert "items" in result[0]
    assert "items" in result[1]
    
    # o1 should have 2 items
    assert len(result[1]["items"]) == 2
    assert result[1]["items"][0]["item_id"] == "item_1"
    
    # o2 should have 1 item
    assert len(result[0]["items"]) == 1


def test_get_order_history_no_orders(monkeypatch):
    """Test order history for user with no orders"""
    
    def mock_get_all_orders():
        return [
            {
                "order_id": "o1",
                "username": "other_user",
                "restaurant_id": "rest_1",
                "status": "pending",
                "created_at": "2026-03-24T12:00:00",
            },
        ]
    
    monkeypatch.setattr(order_service, "get_all_orders", mock_get_all_orders)
    
    result = order_service.get_order_history("jahan")
    
    assert result == []