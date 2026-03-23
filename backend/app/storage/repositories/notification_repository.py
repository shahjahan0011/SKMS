"""Notification Repository"""

import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from typing import List, Dict, Optional
 
from app.storage.repositories.base_csv_repository import BaseCSVRepository
from app.constants import NotificationCSVFields

class notification_repository(BaseCSVRepository):
    """Stores and retrieves notification data"""

    def __init__(self):
        super().__init__("notifications.csv")

    def get_all_notifications(self):
        """returns all notifications from csv"""

        return self._read_all_rows()

    def get_notifications_by_user_id(self, user_id):
        """returns all notifications for a given user"""

        return self._find_rows_by_field(NotificationCSVFields.USER_ID, str(user_id))

    def get_notifications_by_role(self, role):
        """returns all notifications for a given role"""
        return self._find_rows_by_field(NotificationCSVFields.ROLE, str(role))

    def notification_exists(self, event_key):
        """checks if a notification with the same event key already exists"""

        return self._row_exists_by_field(NotificationCSVFields.EVENT_KEY, event_key)

    def create_notification(self, notification):
        """writes a new notification into csv data"""

        if self.notification_exists(notification[NotificationCSVFields.EVENT_KEY]):
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        notification_id = str(uuid4())

        self._write_row([
            notification_id,
            notification[NotificationCSVFields.USER_ID],
            notification[NotificationCSVFields.ROLE],
            notification[NotificationCSVFields.EVENT_TYPE],
            notification[NotificationCSVFields.EVENT_KEY],
            notification[NotificationCSVFields.MESSAGE],
            notification[NotificationCSVFields.ORDER_ID],
            created_at
        ])


        return {
            NotificationCSVFields.ID: notification_id,
            NotificationCSVFields.USER_ID: notification[NotificationCSVFields.USER_ID],
            NotificationCSVFields.ROLE: notification[NotificationCSVFields.ROLE],
            NotificationCSVFields.EVENT_TYPE: notification[NotificationCSVFields.EVENT_TYPE],
            NotificationCSVFields.EVENT_KEY: notification[NotificationCSVFields.EVENT_KEY],
            NotificationCSVFields.MESSAGE: notification[NotificationCSVFields.MESSAGE],
            NotificationCSVFields.ORDER_ID: notification[NotificationCSVFields.ORDER_ID],
            NotificationCSVFields.CREATED_AT: created_at
        }
