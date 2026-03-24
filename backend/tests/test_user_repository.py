"""Test for user reposotory (reading and writing into the csv)"""
import csv
from pathlib import Path

from app.storage.repositories.user_repository import user_repository
from app.constants import UserCSVFields, UserRole 



def setup_test_csv(file_path):
    """create a temporary csv file for testing"""

    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "password", "role"])
        writer.writerow(["bheema", "password123", UserRole.USER.value])
        writer.writerow(["owner1", "ownerpass", "owner"])


def get_test_file_path():
    """return the path for the temporary test csv file"""

    return Path(__file__).resolve().parent / "test_users.csv"


def test_get_all_users():
    """test repository returns all users"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    users = repo.get_all_users()

    assert len(users) == 2
    assert users[0][UserCSVFields.USERNAME] == "bheema"
    assert users[1][UserCSVFields.USERNAME] == "owner1"

    test_file.unlink()


def test_get_user_by_username_valid():
    """test repository returns correct user"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    user = repo.get_user_by_username("bheema")

    assert user is not None
    assert user[UserCSVFields.USERNAME] == "bheema"

    test_file.unlink()


def test_get_user_by_username_invalid():
    """test repository returns none for invalid username"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    user = repo.get_user_by_username("not_real")

    assert user is None

    test_file.unlink()


def test_create_user():
    """test repository adds new user"""

    test_file = get_test_file_path()
    setup_test_csv(test_file)

    repo = user_repository()
    repo.file_path = test_file

    repo.create_user("new_user", "pass123", UserRole.USER.value)

    users = repo.get_all_users()

    assert len(users) == 3
    assert users[2][UserCSVFields.USERNAME] == "new_user"

    test_file.unlink()
    