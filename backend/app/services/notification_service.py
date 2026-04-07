"""Business logic for notifications"""

from app.storage.repositories.notification_repository import NotificationRepository
from app.schemas.notification_schema import NotificationCreate
from app.constants import NotificationEventType, UserRole

from typing import Optional, Dict

class NotificationService:
    """service responsible for notification logic"""

    def __init__(self, notification_repo: NotificationRepository = None):
        """Initialize notification service with optional repository injection"""
        self.notification_repo = (
            notification_repo if notification_repo else NotificationRepository()
        )

    def _create_notification_template(
        self,
        user_id: str,
        order_id: str,
        role: str,
        event_type: str,
        message: str
    ) -> Optional[Dict]:
        """Template Handles ALL the common notification creation logic"""

        event_key = f"{event_type}:{order_id}:{user_id}"

        notification = NotificationCreate(
            user_id=str(user_id),
            role=role,
            event_type=event_type,
            event_key=event_key,
            message=message,
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())



    def notify_order_created(self, user_id, order_id):
        """create notification for successful order creation"""

        return self._create_notification_template(
            user_id=user_id,
            order_id=order_id,
            role=UserRole.CUSTOMER.value,
            event_type=NotificationEventType.ORDER_CREATED.value,
            message=f"Your order {order_id} was created successfully."
        )

    def notify_payment_result(
        self,
        user_id: str,
        order_id: str,
        success: bool
    ) -> Optional[Dict]:
        """Create notification for payment success or failure"""
        event_type = (
            NotificationEventType.PAYMENT_SUCCESS.value
            if success
            else NotificationEventType.PAYMENT_FAILED.value
        )

        message = (
            f"Payment for order {order_id} was successful."
            if success
            else f"Payment for order {order_id} failed."
        )

        return self._create_notification_template(
            user_id=user_id,
            order_id=order_id,
            role=UserRole.CUSTOMER.value,
            event_type=event_type,
            message=message
        )

    def notify_order_status_changed(
        self,
        user_id: str,
        order_id: str,
        new_status: str
    ) -> Optional[Dict]:
        """Create notification for order status changes"""
        event_key = (
            f"{NotificationEventType.ORDER_STATUS_CHANGED.value}:"
            f"{order_id}:{new_status}:{user_id}"
        )

        notification = NotificationCreate(
            user_id=str(user_id),
            role=UserRole.CUSTOMER.value,
            event_type=NotificationEventType.ORDER_STATUS_CHANGED.value,
            event_key=event_key,
            message=f"Your order {order_id} status changed to {new_status}.",
            order_id=str(order_id)
        )

        return self.notification_repo.create_notification(notification.model_dump())

    def notify_manager_new_paid_order(
        self,
        manager_id: str,
        order_id: str
    ) -> Optional[Dict]:
        """Create notification for manager when a new paid order is ready"""
        return self._create_notification_template(
            user_id=manager_id,
            order_id=order_id,
            role=UserRole.MANAGER.value,
            event_type=NotificationEventType.NEW_PAID_ORDER.value,
            message=f"A new paid order {order_id} is ready for preparation."
        )


    # M4: To add admin inventory notifications
    def notify_admin_sold_out(self, item_id: str) -> Optional[Dict]:
        """Create notification for manager when an item hits 0 stock"""
        return self._create_notification_template(
            user_id="system",
            order_id=item_id,
            role=UserRole.MANAGER.value,
            event_type="inventory_sold_out",
            message=f"URGENT: Item {item_id} has completely sold out and is now offline."
        )

    def notify_admin_low_stock(self, item_id: str, remaining_stock: int) -> Optional[Dict]:
        """Create notification for manager when an item is running low"""
        return self._create_notification_template(
            user_id="system",
            order_id=item_id,
            role=UserRole.MANAGER.value,
            event_type="inventory_low_stock",
            message=f"WARNING: Item {item_id} is running low! Only {remaining_stock} left in stock."
        )

    def get_user_notifications(self, user_id: str):
        """return all notifications for a user"""
        return self.notification_repo.get_notifications_by_user_id(user_id)

    def get_role_notifications(self, role: str):
        """return all notifications for a role"""
        return self.notification_repo.get_notifications_by_role(role)
