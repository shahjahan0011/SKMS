"""Tests for BaseCSVRepository"""
import csv
from pathlib import Path
import pytest

from app.storage.repositories.base_csv_repository import BaseCSVRepository


def create_test_csv(file_path, headers, rows):
    """Helper to create test CSV"""
    with open(file_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def test_read_all_rows(tmp_path):
    """test base repository reads all rows from CSV"""

    create_test_csv(tmp_path / "test.csv", ["name", "age"], [["Alice", "30"], ["Bob", "25"]])

    repo = BaseCSVRepository("test.csv", headers=["name", "age"], base_path=tmp_path)

    rows = repo._read_all_rows()

    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"


def test_find_row_by_field(tmp_path):
    """test finding a single row by field value"""

    create_test_csv(tmp_path / "test.csv", ["username", "role"], [["alice", "admin"], ["bob", "user"]])

    repo = BaseCSVRepository("test.csv", headers=["username", "role"], base_path=tmp_path)

    result = repo._find_row_by_field("username", "alice")

    assert result is not None
    assert result["username"] == "alice"
    assert result["role"] == "admin"


def test_find_row_by_field_not_found(tmp_path):
    """test finding non-existent row returns None"""

    create_test_csv(tmp_path / "test.csv", ["username", "role"], [["alice", "admin"]])

    repo = BaseCSVRepository("test.csv", headers=["username", "role"], base_path=tmp_path)

    result = repo._find_row_by_field("username", "nonexistent")

    assert result is None


def test_find_rows_by_field(tmp_path):
    """test finding multiple rows by field value"""

    create_test_csv(
        tmp_path / "test.csv",
        ["username", "role"],
        [["alice", "admin"], ["bob", "admin"], ["charlie", "user"]]
    )

    repo = BaseCSVRepository("test.csv", headers=["username", "role"], base_path=tmp_path)

    results = repo._find_rows_by_field("role", "admin")

    assert len(results) == 2
    assert results[0]["username"] == "alice"
    assert results[1]["username"] == "bob"


def test_row_exists_by_field(tmp_path):
    """test checking if row exists"""

    create_test_csv(tmp_path / "test.csv", ["username"], [["alice"], ["bob"]])

    repo = BaseCSVRepository("test.csv", headers=["username"], base_path=tmp_path)

    assert repo._row_exists_by_field("username", "alice") is True
    assert repo._row_exists_by_field("username", "charlie") is False


def test_write_row(tmp_path):
    """test writing a new row to CSV"""

    create_test_csv(tmp_path / "test.csv", ["username", "role"], [])

    repo = BaseCSVRepository("test.csv", headers=["username", "role"], base_path=tmp_path)

    repo._write_row(["alice", "admin"])

    rows = repo._read_all_rows()
    assert len(rows) == 1
    assert rows[0]["username"] == "alice"


def test_read_all_rows_file_not_found():
    """test error handling for missing file"""

    repo = BaseCSVRepository("nonexistent.csv")

    with pytest.raises(FileNotFoundError):
        repo._read_all_rows()


def test_find_row_by_field_empty_file(tmp_path):
    """test finding row in empty CSV"""

    create_test_csv(tmp_path / "test.csv", ["username", "role"], [])

    repo = BaseCSVRepository("test.csv", headers=["username", "role"], base_path=tmp_path)

    result = repo._find_row_by_field("username", "alice")

    assert result is None


def test_find_rows_by_field_no_matches(tmp_path):
    """test finding rows when no matches exist"""

    create_test_csv(tmp_path / "test.csv", ["role"], [["user"], ["user"]])

    repo = BaseCSVRepository("test.csv", headers=["role"], base_path=tmp_path)

    results = repo._find_rows_by_field("role", "admin")

    assert len(results) == 0
    