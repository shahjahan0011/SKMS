"""Business logic for notifications"""

from app.storage.repositories.notification_repository import notification_repository
from app.schemas.notification_schema import notification_create
from app.constants import NotificationEventType, UserRole



class notification_service:
    """service responsible for notification logic"""

    def __init__(self, notification_repo: notification_repository = None):
        """Initialize notification service with optional repository injection"""
        self.notification_repo = (
            notification_repo if notification_repo else notification_repository()
        )

    def notify_order_created(self, user_id, order_id):
        """create notification for successful order creation"""

        notification = notification_create(
            user_id=str(user_id),
            role=UserRole.CUSTOMER.value,
            event_type=NotificationEventType.ORDER_CREATED.value,
            event_key=f"{NotificationEventType.ORDER_CREATED.value}:{order_id}:{user_id}",
            message=f"Your order {order_id} was created successfully.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_payment_result(self, user_id, order_id, success):
        """create notification for payment success or failure"""

        event_type = NotificationEventType.PAYMENT_SUCCESS.value if success else NotificationEventType.PAYMENT_FAILED.value
        message = (
            f"Payment for order {order_id} was successful."
            if success
            else f"Payment for order {order_id} failed."
        )

        notification = notification_create(
            user_id=str(user_id),
            role=UserRole.CUSTOMER.value,
            event_type=event_type,
            event_key=f"{event_type}:{order_id}:{user_id}",
            message=message,
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_order_status_changed(self, user_id, order_id, new_status):
        """create notification for order status changes"""

        notification = notification_create(
            user_id=str(user_id),
            role=UserRole.CUSTOMER.value,
            event_type=NotificationEventType.ORDER_STATUS_CHANGED.value,
            event_key=f"{NotificationEventType.ORDER_STATUS_CHANGED.value}:{order_id}:{new_status}:{user_id}",
            message=f"Your order {order_id} status changed to {new_status}.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_manager_new_paid_order(self, manager_id, order_id):
        """create notification for manager when a new paid order is ready"""

        notification = notification_create(
            user_id=str(manager_id),
            role=UserRole.MANAGER.value,
            event_type=NotificationEventType.NEW_PAID_ORDER.value,
            event_key=f"{NotificationEventType.NEW_PAID_ORDER.value}:{order_id}:{manager_id}",
            message=f"A new paid order {order_id} is ready for preparation.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def get_user_notifications(self, user_id):
        """return all notifications for a user"""

        return self.notification_repo.get_notifications_by_user_id(user_id)

    def get_role_notifications(self, role):
        """return all notifications for a role"""

        return self.notification_repo.get_notifications_by_role(role)
    