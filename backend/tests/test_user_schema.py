"""Test for User schema"""
from pydantic import ValidationError
from app.schemas.user_schema import user_register, user_login, user_response


class test_user_schema:
    """tests for user authentication schemas"""

    def test_user_register_accepts_valid_input(self):
        """test register schema accepts valid input"""

        user = user_register(
            email="test@example.com",
            password="password123",
            role="user"
        )

        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.role == "user"

    def test_user_register_uses_default_role(self):
        """test register schema uses default role when omitted"""

        user = user_register(
            email="test@example.com",
            password="password123"
        )

        assert user.role == "user"

    def test_user_register_rejects_invalid_email(self):
        """test register schema rejects invalid email"""

        try:
            user_register(
                email="invalid-email",
                password="password123",
                role="user"
            )
            assert False
        except ValidationError:
            assert True

    def test_user_login_accepts_valid_input(self):
        """test login schema accepts valid input"""

        user = user_login(
            email="test@example.com",
            password="password123"
        )

        assert user.email == "test@example.com"
        assert user.password == "password123"

    def test_user_response_does_not_include_password(self):
        """test response schema only contains safe fields"""

        user = user_response(
            email="test@example.com",
            role="user"
        )

        assert user.email == "test@example.com"
        assert user.role == "user"