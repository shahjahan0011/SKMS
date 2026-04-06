"""Tests for Favorite Service"""

from app.services.favorite_service import favorite_service


def setup_favorite_env(tmp_path):
    service = favorite_service

    service.repo.file_path = tmp_path / "favorites.csv"

    with open(service.repo.file_path, mode = "w") as file:
        file.write("user_id,restaurant_id\n")

    return service



def test_add_favorite(tmp_path):
    """test adding a favorite"""

    service = setup_favorite_env(tmp_path)

    service.add_favorite(1, 1)

    data = service.repo.get_all()

    assert len(data) == 1
    assert data[0]["user_id"] == "1"



def test_get_user_favorites(tmp_path):
    """test getting favorites for a user"""

    service = setup_favorite_env(tmp_path)

    service.repo.add_favorite(1, 1)
    service.repo.add_favorite(1, 2)

    result = service.get_user_favorites(1)

    assert len(result) == 2



def test_remove_favorite(tmp_path):
    """test removing a favorite"""

    service = setup_favorite_env(tmp_path)

    service.repo.add_favorite(1, 1)
    service.remove_favorite(1, 1)

    data = service.repo.get_all()

    assert len(data) == 0



def test_add_favorite_invalid_restaurant(tmp_path):
    """test adding favorite with invalid restaurant"""

    service = setup_favorite_env(tmp_path)

    try:
        service.add_favorite(1, 999999)
        assert False
    except ValueError:
        assert True



def test_get_user_favorites_empty(tmp_path):
    """test getting favorites when none exist"""

    service = setup_favorite_env(tmp_path)

    result = service.get_user_favorites(1)

    assert result == []
    