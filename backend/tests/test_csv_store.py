"""Tests for CSVStore class."""

import csv
from app.storage.csv_store import CSVStore

def test_read_csv(tmp_path):
    """Test the read_csv method of CSVStore."""
    temp_file = tmp_path / "test_data.csv"

    # Create a sample CSV file for testing
    test_data = [
        {'id': '1', 'name': 'Burger joint', 'is_active': 'True', 'city': 'New York'},
        {'id': '2', 'name': 'Sushi bar', 'is_active': 'False', 'city': 'San Francisco'},
        {'id': '3', 'name': 'Pizza place', 'is_active': 'True', 'city': 'Chicago'}
    ]

    with open(temp_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'is_active', 'city'])
        writer.writeheader()
        writer.writerows(test_data)

    #Call the method to test it
    result = CSVStore.read_csv(str(temp_file))

    #Assert that the result is as expected
    assert len(result) == 3
    assert result[0]['id'] == '1'
    assert result[0]['name'] == 'Burger joint'
    assert result[1]['is_active'] == 'False'

def test_read_csv_file_not_found():
    """Test the read_csv method when the file is not found."""

    # Call the method with a non-existent file path
    result = CSVStore.read_csv('non_existent_file.csv')

    # Assert that the result is an empty list
    assert result == []
