"""Business logic for notifications"""

from app.storage.repositories.notification_repository import notification_repository
from app.schemas.notification_schema import notification_create


class notification_service:
    """service responsible for notification logic"""

    def __init__(self):
        self.notification_repo = notification_repository()

    def notify_order_created(self, user_id, order_id):
        """create notification for successful order creation"""

        notification = notification_create(
            user_id=str(user_id),
            role="customer",
            event_type="order_created",
            event_key=f"order_created:{order_id}:{user_id}",
            message=f"Your order {order_id} was created successfully.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_payment_result(self, user_id, order_id, success):
        """create notification for payment success or failure"""

        event_type = "payment_success" if success else "payment_failed"
        message = (
            f"Payment for order {order_id} was successful."
            if success
            else f"Payment for order {order_id} failed."
        )

        notification = notification_create(
            user_id=str(user_id),
            role="customer",
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
            role="customer",
            event_type="order_status_changed",
            event_key=f"order_status_changed:{order_id}:{new_status}:{user_id}",
            message=f"Your order {order_id} status changed to {new_status}.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_manager_new_paid_order(self, manager_id, order_id):
        """create notification for manager when a new paid order is ready"""

        notification = notification_create(
            user_id=str(manager_id),
            role="manager",
            event_type="new_paid_order",
            event_key=f"new_paid_order:{order_id}:{manager_id}",
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
    