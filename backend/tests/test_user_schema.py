"""Test for schema"""
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse


def test_UserRegister_accepts_valid_input():
    """test register schema accepts valid input"""

    user = UserRegister(
        username="bheema",
        password="password123",
        role="user"
    )

    assert user.username == "bheema"
    assert user.password == "password123"
    assert user.role == "user"


def test_UserRegister_uses_default_role():
    """test register schema uses default role when omitted"""

    user = UserRegister(
        username="bheema",
        password="password123"
    )

    assert user.role == "user"


def test_UserLogin_accepts_valid_input():
    """test login schema accepts valid input"""

    user = UserLogin(
        username="bheema",
        password="password123"
    )

    assert user.username == "bheema"
    assert user.password == "password123"


def test_UserResponse_contains_only_safe_fields():
    """test response schema contains only safe fields"""

    user = UserResponse(
        username="bheema",
        role="user"
    )

    assert user.username == "bheema"
    assert user.role == "user"


def test_UserResponse_has_no_password_field():
    """test response schema does not expose password"""

    user = UserResponse(
        username="bheema",
        role="user"
    )

    assert not hasattr(user, "password")
