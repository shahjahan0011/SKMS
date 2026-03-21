"""Tests for Notification Repository"""

from pathlib import Path
from app.storage.repositories.notification_repository import notification_repository


def write_notification_header(file_path):
    """creates csv header for notification tests"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        file.write("id,user_id,role,event_type,event_key,message,order_id,created_at\n")


def test_create_notification(tmp_path):
    """creates and stores a notification"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = notification_repository()
    repo.file_path = file_path

    notification = {
        "user_id": "1",
        "role": "customer",
        "event_type": "order_created",
        "event_key": "order_created:101:1",
        "message": "Your order 101 was created successfully.",
        "order_id": "101"
    }

    result = repo.create_notification(notification)

    assert result is not None
    assert result["user_id"] == "1"
    assert result["role"] == "customer"
    assert result["event_type"] == "order_created"
    assert result["event_key"] == "order_created:101:1"
    assert result["order_id"] == "101"


def test_create_notification_prevents_duplicates(tmp_path):
    """does not create duplicate notifications for the same event"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = notification_repository()
    repo.file_path = file_path

    notification = {
        "user_id": "1",
        "role": "customer",
        "event_type": "order_created",
        "event_key": "order_created:101:1",
        "message": "Your order 101 was created successfully.",
        "order_id": "101"
    }

    first = repo.create_notification(notification)
    second = repo.create_notification(notification)

    assert first is not None
    assert second is None

    notifications = repo.get_notifications_by_user_id("1")
    assert len(notifications) == 1


def test_get_notifications_by_user_id(tmp_path):
    """gets notifications belonging to one user only"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = notification_repository()
    repo.file_path = file_path

    repo.create_notification({
        "user_id": "1",
        "role": "customer",
        "event_type": "order_created",
        "event_key": "order_created:101:1",
        "message": "Your order 101 was created successfully.",
        "order_id": "101"
    })

    repo.create_notification({
        "user_id": "2",
        "role": "manager",
        "event_type": "new_paid_order",
        "event_key": "new_paid_order:101:2",
        "message": "A new paid order 101 is ready.",
        "order_id": "101"
    })

    result = repo.get_notifications_by_user_id("1")

    assert len(result) == 1
    assert result[0]["user_id"] == "1"


def test_get_notifications_by_role(tmp_path):
    """gets notifications belonging to one role only"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = notification_repository()
    repo.file_path = file_path

    repo.create_notification({
        "user_id": "1",
        "role": "customer",
        "event_type": "order_created",
        "event_key": "order_created:101:1",
        "message": "Your order 101 was created successfully.",
        "order_id": "101"
    })

    repo.create_notification({
        "user_id": "2",
        "role": "manager",
        "event_type": "new_paid_order",
        "event_key": "new_paid_order:101:2",
        "message": "A new paid order 101 is ready.",
        "order_id": "101"
    })

    result = repo.get_notifications_by_role("manager")

    assert len(result) == 1
    assert result[0]["role"] == "manager"