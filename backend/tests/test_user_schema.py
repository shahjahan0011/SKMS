"""Test for schema"""
from app.schemas.user_schema import user_login, user_register, user_response


def test_user_register_accepts_valid_input():
    """test register schema accepts valid input"""

    user = user_register(
        username="bheema",
        password="password123",
        role="user"
    )

    assert user.username == "bheema"
    assert user.password == "password123"
    assert user.role == "user"


def test_user_register_uses_default_role():
    """test register schema uses default role when omitted"""

    user = user_register(
        username="bheema",
        password="password123"
    )

    assert user.role == "user"


def test_user_login_accepts_valid_input():
    """test login schema accepts valid input"""

    user = user_login(
        username="bheema",
        password="password123"
    )

    assert user.username == "bheema"
    assert user.password == "password123"


def test_user_response_contains_only_safe_fields():
    """test response schema contains only safe fields"""

    user = user_response(
        username="bheema",
        role="user"
    )

    assert user.username == "bheema"
    assert user.role == "user"


def test_user_response_has_no_password_field():
    """test response schema does not expose password"""

    user = user_response(
        username="bheema",
        role="user"
    )

    assert not hasattr(user, "password")
