"""Tests for Favorite Router"""

from fastapi.testclient import TestClient
from app.main import app
from app.routers.favorite_router import favorite_service

client = TestClient(app)


def setup_router_env(tmp_path):
    favorite_service.repo.file_path = tmp_path / "favorites.csv"

    with open(favorite_service.repo.file_path, mode = "w") as file:
        file.write("user_id,restaurant_id\n")



def test_add_favorite(tmp_path):
    """test adding favorite from router"""

    setup_router_env(tmp_path)

    response = client.post("/favorites?user_id=1&restaurant_id=1")

    assert response.status_code == 200

    data = favorite_service.repo.get_all()
    assert len(data) == 1



def test_get_user_favorites(tmp_path):
    """test getting favorites for user"""

    setup_router_env(tmp_path)

    favorite_service.repo.add_favorite(1, 1)
    favorite_service.repo.add_favorite(1, 2)

    response = client.get("/favorites/user/1")

    assert response.status_code == 200
    assert len(response.json()) == 2



def test_remove_favorite(tmp_path):
    """test removing favorite"""

    setup_router_env(tmp_path)

    favorite_service.repo.add_favorite(1, 1)

    response = client.delete("/favorites?user_id=1&restaurant_id=1")

    assert response.status_code == 200

    data = favorite_service.repo.get_all()
    assert len(data) == 0



def test_add_favorite_invalid_restaurant(tmp_path):
    """test adding favorite with invalid restaurant"""

    setup_router_env(tmp_path)

    response = client.post("/favorites?user_id=1&restaurant_id=999999")

    assert response.status_code == 400
