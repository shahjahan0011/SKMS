"""Business logic for user authentication"""
from app.storage.repositories.user_repository import user_repository


class auth_service:
    """service responsible for authentication logic"""

    def __init__(self):
        self.user_repo = user_repository()

    def register_user(self, username, password, role="user"):
        """register a new user"""

        if not username:
            raise ValueError("Please enter a username")
        if not password:
            raise ValueError("Please enter password")

        existing_user = self.user_repo.get_user_by_username(username)

        if existing_user:
            raise ValueError("username already exists")

        self.user_repo.create_user(username, password, role)

        return {
            "username": username,
            "role": role
        }

    def login_user(self, username, password):
        """authenticate a user"""

        user = self.user_repo.get_user_by_username(username)

        if user is None:
            raise ValueError("invalid username or password")

        if user["password"] != password:
            raise ValueError("invalid username or password")

        return {
            "username": user["username"],
            "role": user["role"]
        }
