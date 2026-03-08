"""user reposotory that handles the user data (reading and writing from the user.csv)"""
import csv
from pathlib import Path


class user_repository:
    """repository responsible for reading and writing user data"""

    def __init__(self):
        self.file_path = Path("app/storage/data/users.csv")

    def get_all_users(self):
        """return all users from csv storage"""

        users = []

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                users.append(row)

        return users

    def get_user_by_username(self, username):
        """return a user if the username exists"""

        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["username"] == username:
                    return row

        return None

    def create_user(self, username, password, role):
        """add a new user to csv storage"""

        with open(self.file_path, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role])
