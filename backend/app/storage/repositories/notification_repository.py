"""Notification Repository"""

import csv
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


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
                if row["user_id"] == str(user_id):
                    notifications.append(row)

        return notifications

    def get_notifications_by_role(self, role):
        """returns all notifications for a given role"""

        notifications = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["role"] == str(role):
                    notifications.append(row)

        return notifications

    def notification_exists(self, event_key):
        """checks if a notification with the same event key already exists"""

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["event_key"] == event_key:
                    return True

        return False

    def create_notification(self, notification):
        """writes a new notification into csv data"""

        if self.notification_exists(notification["event_key"]):
            return None

        created_at = datetime.now(timezone.utc).isoformat()
        notification_id = str(uuid4())

        with open(self.file_path, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                notification_id,
                notification["user_id"],
                notification["role"],
                notification["event_type"],
                notification["event_key"],
                notification["message"],
                notification["order_id"],
                created_at
            ])

        return {
            "id": notification_id,
            "user_id": notification["user_id"],
            "role": notification["role"],
            "event_type": notification["event_type"],
            "event_key": notification["event_key"],
            "message": notification["message"],
            "order_id": notification["order_id"],
            "created_at": created_at
        }