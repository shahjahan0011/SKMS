"""Menu repository for fetching menu data."""
import csv
from typing import List, Dict, Optional
from app.storage.csv_store import CSVStore

# pylint: disable=too-few-public-methods
class MenuRepository:
    """Repository for fetching menu data."""
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, "..", "data", "menus.csv")
        self.file_path = os.path.abspath(self.file_path)
        # app/storage/repositories/../data/menus.csv

    def get_all(self) -> List[Dict]:
        """Fetch all menu data from the CSV file."""
        return CSVStore.read_csv(self.file_path)

    def get_menu_by_restaurant(self, restaurant_id: str) -> List[Dict]:
        """Fetch menu items for a specific restaurant from the CSV file."""
        all_menus = self.get_all()

        return [
            item for item in all_menus
            if str(item.get("id")) == str(restaurant_id)
            ]
    
    def get_menu_item_by_id(self, id: str) -> Optional[dict]:
        with open(self.file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_id = row.get("id")
                if row_id == id:
                    return row
        return None
