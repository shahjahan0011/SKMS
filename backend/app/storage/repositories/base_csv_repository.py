"""Base repository for CSV storage operations"""
import csv
from pathlib import Path
from typing import List, Dict, Optional, Callable
 
 
class BaseCSVRepository:
    """Base class for CSV-based repositories. Eliminates duplicated CSV reading/writing code"""
 
    def __init__(self, csv_filename: str):
        """Initialize repository with CSV file path"""
        self.file_path = (
            Path(__file__).resolve().parents[1] / "data" / csv_filename
        )
 
    def _read_all_rows(self) -> List[Dict[str, str]]:
        """Read all rows from CSV file"""
        rows = []
        with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                rows.append(row)
        return rows
 
    def _find_rows_by_field(
        self,
        field_name: str,
        field_value: str
    ) -> List[Dict[str, str]]:
        """Find all rows matching a field value"""
        rows = self._read_all_rows()
        return [row for row in rows if row.get(field_name) == str(field_value)]
 
    def _find_row_by_field(
        self,
        field_name: str,
        field_value: str
    ) -> Optional[Dict[str, str]]:
        """Find first row matching a field value"""
        rows = self._read_all_rows()
        for row in rows:
            if row.get(field_name) == str(field_value):
                return row
        return None
 
    def _row_exists_by_field(
        self,
        field_name: str,
        field_value: str
    ) -> bool:
        """Check if a row with matching field value exists"""
        return self._find_row_by_field(field_name, field_value) is not None
 
    def _write_row(self, row_data: List[str]) -> None:
        """Append a row to the CSV file"""
        with open(self.file_path, mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row_data)
 