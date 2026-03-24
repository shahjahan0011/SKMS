"""Unit test for notification service"""

from app.services.notification_service import notification_service
from app.constants import NotificationEventType, UserRole

class stub_notification_repository:
    """stub repository for notification service tests"""

    def __init__(self):
        self.notifications = []

    def create_notification(self, notification):
        """store notification in memory"""

        self.notifications.append(notification)
        return notification

    def get_notifications_by_user_id(self, user_id):
        """return notifications for one user"""

        results = []

        for notification in self.notifications:
            if notification["user_id"] == str(user_id):
                results.append(notification)

        return results

    def get_notifications_by_role(self, role):
        """return notifications for one role"""

        results = []

        for notification in self.notifications:
            if notification["role"] == str(role):
                results.append(notification)

        return results


def test_notify_order_created():
    """test order creation notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_order_created("1", "101")

    assert result["user_id"] == "1"
    assert result["role"] == UserRole.CUSTOMER.value
    assert result["event_type"] == NotificationEventType.ORDER_CREATED.value
    assert result["event_key"] == f"{NotificationEventType.ORDER_CREATED.value}:101:1" 
    assert result["order_id"] == "101"


def test_notify_payment_success():
    """test payment success notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_payment_result("1", "101", True)

    assert result["event_type"] == NotificationEventType.PAYMENT_SUCCESS.value  
    assert result["message"] == "Payment for order 101 was successful."


def test_notify_payment_failure():
    """test payment failure notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_payment_result("1", "101", False)

    assert result["event_type"] == NotificationEventType.PAYMENT_FAILED.value
    assert result["message"] == "Payment for order 101 failed."


def test_notify_order_status_changed():
    """test order status change notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_order_status_changed("1", "101", "preparing")

    assert result["event_type"] == NotificationEventType.ORDER_STATUS_CHANGED.value
    assert result["event_key"] == f"{NotificationEventType.ORDER_STATUS_CHANGED.value}:101:preparing:1"
    assert result["message"] == "Your order 101 status changed to preparing."


def test_notify_manager_new_paid_order():
    """test manager gets notification for new paid order"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_manager_new_paid_order("20", "101")

    assert result["user_id"] == "20"
    assert result["role"] == UserRole.MANAGER.value
    assert result["event_type"] == NotificationEventType.NEW_PAID_ORDER.value
    assert result["message"] == "A new paid order 101 is ready for preparation."


def test_get_user_notifications():
    """test retrieving notifications for one user"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    service.notify_order_created("1", "101")
    service.notify_payment_result("2", "102", True)

    result = service.get_user_notifications("1")

    assert len(result) == 1
    assert result[0]["user_id"] == "1"


def test_get_role_notifications():
    """test retrieving notifications for one role"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    service.notify_order_created("1", "101")
    service.notify_manager_new_paid_order("20", "101")

    result = service.get_role_notifications(UserRole.MANAGER.value)  

    assert len(result) == 1
    assert result[0]["role"] == UserRole.MANAGER.value  

def test_create_notification_template():
    """test template method creates notification correctly"""
    
    service = notification_service()
    service.notification_repo = stub_notification_repository()
    
    result = service._create_notification_template(
        user_id="123",
        order_id="456",
        role=UserRole.CUSTOMER.value,
        event_type=NotificationEventType.ORDER_CREATED.value,
        message="Test message"
    )
    
    assert result is not None
    assert result["user_id"] == "123"
    assert result["order_id"] == "456"
    assert result["role"] == UserRole.CUSTOMER.value
    assert result["event_type"] == NotificationEventType.ORDER_CREATED.value
    assert result["message"] == "Test message"
    assert NotificationEventType.ORDER_CREATED.value in result["event_key"]


def test_template_method_generates_correct_event_key():
    """test template method creates properly formatted event key"""
    
    service = notification_service()
    service.notification_repo = stub_notification_repository()
    
    result = service._create_notification_template(
        user_id="u1",
        order_id="o1",
        role=UserRole.MANAGER.value,
        event_type=NotificationEventType.NEW_PAID_ORDER.value,
        message="Test"
    )
    
    expected_key = f"{NotificationEventType.NEW_PAID_ORDER.value}:o1:u1"
    assert result["event_key"] == expected_key


def test_all_notify_methods_use_consistent_structure():
    """test that all notification methods produce consistent output structure"""
    
    service = notification_service()
    service.notification_repo = stub_notification_repository()
    
    # Test multiple notification types
    results = [
        service.notify_order_created("u1", "o1"),
        service.notify_payment_result("u2", "o2", True),
        service.notify_order_status_changed("u3", "o3", "delivered"),
        service.notify_manager_new_paid_order("m1", "o4")
    ]
    
    # All should have same structure
    for result in results:
        assert "user_id" in result
        assert "order_id" in result
        assert "role" in result
        assert "event_type" in result
        assert "event_key" in result
        assert "message" in result