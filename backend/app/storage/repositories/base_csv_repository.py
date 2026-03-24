import csv
import threading
from pathlib import Path
from typing import List, Dict, Optional


class BaseCSVRepository:
    """Base class for CSV-based repositories with thread safety and auto-headers."""
    
    _file_lock = threading.Lock()

    def __init__(self, csv_filename: str, headers: List[str]):
        """Initialize repository with CSV file path and required headers"""
        self.file_path = (
            Path(__file__).resolve().parents[1] / "data" / csv_filename
        )
        self.headers = headers
        self._ensure_file_and_headers()

    def _ensure_file_and_headers(self):
        """Creates the file and writes headers if it doesn't exist."""
        with self._file_lock:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if not self.file_path.exists() or self.file_path.stat().st_size == 0:
                with open(self.file_path, mode="w", encoding="utf-8", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(self.headers)

    def _read_all_rows(self) -> List[Dict[str, str]]:
        """Read all rows from CSV file safely."""
        rows = []
        with self._file_lock:
            try:
                with open(self.file_path, mode="r", encoding="utf-8", newline="") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        rows.append(row)
                return rows
            except FileNotFoundError:
                return []

    def _find_rows_by_field(self, field_name: str, field_value: str) -> List[Dict[str, str]]:
        rows = self._read_all_rows()
        return [row for row in rows if row.get(field_name) == str(field_value)]

    def _find_row_by_field(self, field_name: str, field_value: str) -> Optional[Dict[str, str]]:
        rows = self._read_all_rows()
        for row in rows:
            if row.get(field_name) == str(field_value):
                return row
        return None

    def _row_exists_by_field(self, field_name: str, field_value: str) -> bool:
        return self._find_row_by_field(field_name, field_value) is not None

    def _write_row(self, row_data: List[str]) -> None:
        """Append a row to the CSV file safely."""
        with self._file_lock:
            with open(self.file_path, mode="a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(row_data)
