"""user reposotory that handles the user data (reading and writing from the user.csv)"""
import csv
from pathlib import Path
from typing import Optional, Dict

from app.storage.repositories.base_csv_repository import BaseCSVRepository
from app.constants import UserCSVFields


class user_repository(BaseCSVRepository):
    """repository responsible for reading and writing user data"""

    def __init__(self):
        super().__init__("users.csv")


    def get_all_users(self):
        """return all users from csv storage"""

        return self._read_all_rows()


    def get_user_by_username(self, username: str) -> Optional[Dict[str, str]]:
        """return a user if the username exists"""

        return self._find_row_by_field(UserCSVFields.USERNAME, username)


    def create_user(self, username: str, password: str, role: str) -> None:
        """add a new user to csv storage"""

        self._write_row([username, password, role])

    def get_users_by_role(self, role: str):
        """return all users with a specific role"""
        return self._find_rows_by_field(UserCSVFields.ROLE, role)
 
    def user_exists(self, username: str) -> bool:
        """check if a user exists"""
        return self._row_exists_by_field(UserCSVFields.USERNAME, username)
