"""Tests for Notification Repository"""

from pathlib import Path
from app.storage.repositories.notification_repository import NotificationRepository
from app.constants import UserRole, NotificationEventType, NotificationCSVFields 


def write_notification_header(file_path):
    """creates csv header for notification tests"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        file.write("id,user_id,role,event_type,event_key,message,order_id,created_at\n")


def test_create_notification(tmp_path):
    """creates and stores a notification"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = NotificationRepository()
    repo.file_path = file_path

    notification = {
        NotificationCSVFields.USER_ID: "1",  
        NotificationCSVFields.ROLE: UserRole.CUSTOMER.value, 
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.ORDER_CREATED.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.ORDER_CREATED.value}:101:1",  
        NotificationCSVFields.MESSAGE: "Your order 101 was created successfully.",  
        NotificationCSVFields.ORDER_ID: "101"  
    }

    result = repo.create_notification(notification)

    assert result is not None
    assert result[NotificationCSVFields.USER_ID] == "1" 
    assert result[NotificationCSVFields.ROLE] == UserRole.CUSTOMER.value 
    assert result[NotificationCSVFields.EVENT_TYPE] == NotificationEventType.ORDER_CREATED.value  
    assert result[NotificationCSVFields.EVENT_KEY] == f"{NotificationEventType.ORDER_CREATED.value}:101:1"  
    assert result[NotificationCSVFields.ORDER_ID] == "101"  


def test_create_notification_prevents_duplicates(tmp_path):
    """does not create duplicate notifications for the same event"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = NotificationRepository()
    repo.file_path = file_path

    notification = {
        NotificationCSVFields.USER_ID: "1",  
        NotificationCSVFields.ROLE: UserRole.CUSTOMER.value,  
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.ORDER_CREATED.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.ORDER_CREATED.value}:101:1", 
        NotificationCSVFields.MESSAGE: "Your order 101 was created successfully.",  
        NotificationCSVFields.ORDER_ID: "101" 
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

    repo = NotificationRepository()
    repo.file_path = file_path

    repo.create_notification({
        NotificationCSVFields.USER_ID: "1", 
        NotificationCSVFields.ROLE: UserRole.CUSTOMER.value,  
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.ORDER_CREATED.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.ORDER_CREATED.value}:101:1",  
        NotificationCSVFields.MESSAGE: "Your order 101 was created successfully.",  
        NotificationCSVFields.ORDER_ID: "101"  
    })

    repo.create_notification({
        NotificationCSVFields.USER_ID: "2",  
        NotificationCSVFields.ROLE: UserRole.MANAGER.value,  
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.NEW_PAID_ORDER.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.NEW_PAID_ORDER.value}:101:2",  
        NotificationCSVFields.MESSAGE: "A new paid order 101 is ready.",  
        NotificationCSVFields.ORDER_ID: "101"  

    })

    result = repo.get_notifications_by_user_id("1")

    assert len(result) == 1
    assert result[0][NotificationCSVFields.USER_ID] == "1"


def test_get_notifications_by_role(tmp_path):
    """gets notifications belonging to one role only"""

    file_path = tmp_path / "notifications.csv"
    write_notification_header(file_path)

    repo = NotificationRepository()
    repo.file_path = file_path

    repo.create_notification({
        NotificationCSVFields.USER_ID: "1",  
        NotificationCSVFields.ROLE: UserRole.CUSTOMER.value,  
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.ORDER_CREATED.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.ORDER_CREATED.value}:101:1",  
        NotificationCSVFields.MESSAGE: "Your order 101 was created successfully.",  
        NotificationCSVFields.ORDER_ID: "101"  
    })

    repo.create_notification({
        NotificationCSVFields.USER_ID: "2",  
        NotificationCSVFields.ROLE: UserRole.MANAGER.value,  
        NotificationCSVFields.EVENT_TYPE: NotificationEventType.NEW_PAID_ORDER.value,  
        NotificationCSVFields.EVENT_KEY: f"{NotificationEventType.NEW_PAID_ORDER.value}:101:2",  
        NotificationCSVFields.MESSAGE: "A new paid order 101 is ready.",  
        NotificationCSVFields.ORDER_ID: "101"  
    })


    result = repo.get_notifications_by_role(UserRole.MANAGER.value)

    assert len(result) == 1
    assert result[0][NotificationCSVFields.ROLE] == UserRole.MANAGER.value  
