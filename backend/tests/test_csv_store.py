"""Tests for CSVStore class."""
import textwrap
# pylint: skip-file
from app.storage.csv_store import CSVStore
def test_read_csv():
    """Test the read_csv method of CSVStore."""
    # Create a sample CSV file for testing
    sample_csv_content = textwrap.dedent("""\
        name,location,cuisine
        Pizza Place,New York,Italian
        Sushi Spot,San Francisco,Japanese""")

    sample_csv_path = 'sample_restaurants.csv'
    with open(sample_csv_path, 'w', encoding='utf-8') as f:
        f.write(sample_csv_content)

    # Test reading the CSV file
    expected_output = [
        {'name': 'Pizza Place', 'location': 'New York', 'cuisine': 'Italian'},
        {'name': 'Sushi Spot', 'location': 'San Francisco', 'cuisine': 'Japanese'}
    ]
    assert CSVStore.read_csv(sample_csv_path) == expected_output
