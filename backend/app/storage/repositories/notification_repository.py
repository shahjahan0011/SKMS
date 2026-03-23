"""Notification Repository"""

import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.constants import NotificationCSVFields

class notification_repository:
    """Stores and retrieves notification data"""

    def __init__(self):
        self.file_path = Path(__file__).resolve().parents[1] / "data" / "notifications.csv"

    def get_all_notifications(self):
        """returns all notifications from csv"""

        notifications = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                notifications.append(row)

        return notifications

    def get_notifications_by_user_id(self, user_id):
        """returns all notifications for a given user"""

        notifications = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row[NotificationCSVFields.USER_ID] == str(user_id):
                    notifications.append(row)

        return notifications

    def get_notifications_by_role(self, role):
        """returns all notifications for a given role"""

        notifications = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row[NotificationCSVFields.ROLE] == str(role):
                    notifications.append(row)

        return notifications

    def notification_exists(self, event_key):
        """checks if a notification with the same event key already exists"""

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row[NotificationCSVFields.EVENT_KEY] == event_key:
                    return True

        return False

    def create_notification(self, notification):
        """writes a new notification into csv data"""

        if self.notification_exists(notification[NotificationCSVFields.EVENT_KEY]):
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        notification_id = str(uuid4())

        with open(self.file_path, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
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
