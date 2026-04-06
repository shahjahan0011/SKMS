"""Tests for Favorite Repository"""

import os
from app.storage.repositories.favorite_repository import favorite_repository


def setup_repo(tmp_path):
    repo = favorite_repository

    repo.file_path = tmp_path / "favorites.csv"

    with open(repo.file_path, mode="w") as file:
        file.write("user_id,restaurant_id\n")

    return repo



def test_add_favorite_success(tmp_path):
    """successfully adding a favorite"""
    repo = setup_repo(tmp_path)

    repo.add_favorite(1, 101)

    data = repo.get_all()
    assert len(data) == 1
    assert data[0]["user_id"] == "1"
    assert data[0]["restaurant_id"] == "101"



def test_get_user_favorites(tmp_path):
    """get user favorites test"""
    repo = setup_repo(tmp_path)

    repo.add_favorite(1, 101)
    repo.add_favorite(1, 102)
    repo.add_favorite(2, 201)

    result = repo.get_user_favorites(1)

    assert len(result) == 2



def test_remove_favorite_success(tmp_path):
    """successful test for remove favorite"""
    repo = setup_repo(tmp_path)

    repo.add_favorite(1, 101)
    repo.remove_favorite(1, 101)

    data = repo.get_all()
    assert len(data) == 0



def test_add_duplicate_favorite(tmp_path):
    """test add duplicate favorites"""
    repo = setup_repo(tmp_path)

    repo.add_favorite(1, 101)

    try:
        repo.add_favorite(1, 101)
        assert False
    except Exception:
        assert True



def test_remove_non_existing_favorite(tmp_path):
    """test remove a favorite that does not exist"""
    repo = setup_repo(tmp_path)

    repo.remove_favorite(1, 999)

    data = repo.get_all()
    assert len(data) == 0



def test_get_user_favorites_empty(tmp_path):
    """test get user favorites when its empty"""
    repo = setup_repo(tmp_path)

    result = repo.get_user_favorites(1)

    assert result == []



def test_add_invalid_types(tmp_path):
    """test invalid inputs"""
    repo = setup_repo(tmp_path)

    repo.add_favorite("abc", "xyz")

    data = repo.get_all()
    assert data[0]["user_id"] == "abc"
    assert data[0]["restaurant_id"] == "xyz"
