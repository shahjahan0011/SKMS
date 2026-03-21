"""Unit test for notification service"""

from app.services.notification_service import notification_service


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
    assert result["role"] == "customer"
    assert result["event_type"] == "order_created"
    assert result["event_key"] == "order_created:101:1"
    assert result["order_id"] == "101"


def test_notify_payment_success():
    """test payment success notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_payment_result("1", "101", True)

    assert result["event_type"] == "payment_success"
    assert result["message"] == "Payment for order 101 was successful."


def test_notify_payment_failure():
    """test payment failure notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_payment_result("1", "101", False)

    assert result["event_type"] == "payment_failed"
    assert result["message"] == "Payment for order 101 failed."


def test_notify_order_status_changed():
    """test order status change notification"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_order_status_changed("1", "101", "preparing")

    assert result["event_type"] == "order_status_changed"
    assert result["event_key"] == "order_status_changed:101:preparing:1"
    assert result["message"] == "Your order 101 status changed to preparing."


def test_notify_manager_new_paid_order():
    """test manager gets notification for new paid order"""

    service = notification_service()
    service.notification_repo = stub_notification_repository()

    result = service.notify_manager_new_paid_order("20", "101")

    assert result["user_id"] == "20"
    assert result["role"] == "manager"
    assert result["event_type"] == "new_paid_order"
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

    result = service.get_role_notifications("manager")

    assert len(result) == 1
    assert result[0]["role"] == "manager"
    