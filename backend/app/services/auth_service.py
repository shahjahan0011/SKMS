"""Business logic for user authentication"""
from app.storage.repositories.user_repository import UserRepository 
from app.constants import UserRole, UserCSVFields, ErrorMessages


class AuthService:
    """service responsible for authentication logic"""

    def __init__(self, user_repo: UserRepository = None):
        """Initialize auth service with optional repository injection"""
        self.user_repo = user_repo if user_repo else UserRepository()

    def register_user(self, username, password, role=UserRole.USER.value):
        """register a new user"""

        if not username:
            raise ValueError(ErrorMessages.USERNAME_REQUIRED)
        if not password:
            raise ValueError(ErrorMessages.PASSWORD_REQUIRED)

        existing_user = self.user_repo.get_user_by_username(username)

        if existing_user:
            raise ValueError(ErrorMessages.USERNAME_EXISTS)

        self.user_repo.create_user(username, password, role)

        return {
            UserCSVFields.USERNAME: username,
            UserCSVFields.ROLE: role
        }

    def login_user(self, username, password):
        """authenticate a user"""

        user = self.user_repo.get_user_by_username(username)

        if user is None:
            raise ValueError(ErrorMessages.INVALID_CREDENTIALS)

        if user[UserCSVFields.PASSWORD] != password:
            raise ValueError(ErrorMessages.INVALID_CREDENTIALS)

        return {
            UserCSVFields.USERNAME: user[UserCSVFields.USERNAME],
            UserCSVFields.ROLE: user[UserCSVFields.ROLE]
        }

    def check_role(self, username, required_role):
        """check whether a user has the required role"""

        user = self.user_repo.get_user_by_username(username)

        if user is None:
            raise ValueError(ErrorMessages.USER_NOT_FOUND)

        if user[UserCSVFields.ROLE] != required_role:
            raise PermissionError(ErrorMessages.INSUFFICIENT_PERMISSIONS)

        return True
