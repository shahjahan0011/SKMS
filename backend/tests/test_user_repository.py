import csv
from pathlib import Path

from app.storage.repositories.user_repository import user_repository


def setup_test_csv(file_path):
    """create a temporary csv file for testing"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])
        writer.writerow(["bheema", "password123", "user"])
        writer.writerow(["owner1", "ownerpass", "owner"])


def test_get_all_users():
    """test repository returns all users"""

    test_file = Path("tests/test_users.csv")
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    users = repo.get_all_users()

    assert len(users) == 2
    assert users[0]["username"] == "bheema"
    assert users[1]["username"] == "owner1"

    test_file.unlink()


def test_get_user_by_username_valid():
    """test repository returns correct user"""

    test_file = Path("tests/test_users.csv")
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    user = repo.get_user_by_username("bheema")

    assert user is not None
    assert user["username"] == "bheema"

    test_file.unlink()


def test_get_user_by_username_invalid():
    """test repository returns none for invalid username"""

    test_file = Path("tests/test_users.csv")
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    user = repo.get_user_by_username("not_real")

    assert user is None

    test_file.unlink()


def test_create_user():
    """test repository adds new user"""

    test_file = Path("tests/test_users.csv")
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    repo.create_user("new_user", "pass123", "user")

    users = repo.get_all_users()

    assert len(users) == 3
    assert users[2]["username"] == "new_user"

    test_file.unlink()