import csv
from pathlib import Path

from app.services.auth_service import auth_service


def setup_test_csv(file_path):
    """create temporary user csv"""

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])
        writer.writerow(["bheema", "password123", "user"])


def get_test_file_path():
    return Path(__file__).resolve().parent / "test_users.csv"


def test_register_user():
    """test registering a new user"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    service = auth_service()
    service.user_repo.file_path = test_file

    result = service.register_user("new_user", "pass123")

    assert result["username"] == "new_user"
    assert result["role"] == "user"

    test_file.unlink()


def test_register_duplicate_user():
    """test duplicate username rejection"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    service = auth_service()
    service.user_repo.file_path = test_file

    try:
        service.register_user("bheema", "pass123")
        assert False
    except ValueError:
        assert True

    test_file.unlink()


def test_login_user_success():
    """test successful login"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    service = auth_service()
    service.user_repo.file_path = test_file

    result = service.login_user("bheema", "password123")

    assert result["username"] == "bheema"
    assert result["role"] == "user"

    test_file.unlink()


def test_login_user_invalid_password():
    """test login fails with incorrect password"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    service = auth_service()
    service.user_repo.file_path = test_file

    try:
        service.login_user("bheema", "wrongpass")
        assert False
    except ValueError:
        assert True

    test_file.unlink()