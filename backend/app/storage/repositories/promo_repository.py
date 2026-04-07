"""Promo Code Repository"""

from datetime import datetime, timezone
from typing import List, Dict, Optional

from app.storage.repositories.base_csv_repository import BaseCSVRepository
from app.constants import PromoCSVFields


class PromoRepository(BaseCSVRepository):
    """Stores and retrieves promo code data"""

    def __init__(self):
        headers = [
            PromoCSVFields.CODE,
            PromoCSVFields.DISCOUNT_PERCENT,
            PromoCSVFields.MAX_USES,
            PromoCSVFields.TIMES_USED,
            PromoCSVFields.ACTIVE,
            PromoCSVFields.CREATED_AT,
        ]
        super().__init__("promo_codes.csv", headers=headers)

    def get_all_promos(self) -> List[Dict[str, str]]:
        """returns all promo codes from csv"""
        return self._read_all_rows()

    def get_promo_by_code(self, code: str) -> Optional[Dict[str, str]]:
        """returns a promo code if it exists"""
        return self._find_row_by_field(PromoCSVFields.CODE, code.upper())

    def promo_exists(self, code: str) -> bool:
        """checks if a promo code already exists"""
        return self._row_exists_by_field(PromoCSVFields.CODE, code.upper())

    def create_promo(self, code: str, discount_percent: int, max_uses: int) -> Dict[str, str]:
        """writes a new promo code into csv data"""
        created_at = datetime.now(timezone.utc).isoformat()
        normalized_code = code.upper()

        self._write_row([
            normalized_code,
            str(discount_percent),
            str(max_uses),
            "0",
            "true",
            created_at
        ])

        return {
            PromoCSVFields.CODE: normalized_code,
            PromoCSVFields.DISCOUNT_PERCENT: str(discount_percent),
            PromoCSVFields.MAX_USES: str(max_uses),
            PromoCSVFields.TIMES_USED: "0",
            PromoCSVFields.ACTIVE: "true",
            PromoCSVFields.CREATED_AT: created_at
        }

    def delete_promo(self, code: str) -> bool:
        """deletes a promo code by overwriting csv without it"""
        rows = self._read_all_rows()
        normalized_code = code.upper()
        filtered = [row for row in rows if row.get(PromoCSVFields.CODE) != normalized_code]

        if len(filtered) == len(rows):
            return False

        self._rewrite_all_rows(filtered)
        return True

    def set_active_status(self, code: str, active: bool) -> Optional[Dict[str, str]]:
        """toggles the active status of a promo code"""
        rows = self._read_all_rows()
        normalized_code = code.upper()
        updated = None

        for row in rows:
            if row.get(PromoCSVFields.CODE) == normalized_code:
                row[PromoCSVFields.ACTIVE] = "true" if active else "false"
                updated = row
                break

        if updated is None:
            return None

        self._rewrite_all_rows(rows)
        return updated

    def increment_times_used(self, code: str) -> Optional[Dict[str, str]]:
        """increments the times_used counter for a promo code"""
        rows = self._read_all_rows()
        normalized_code = code.upper()
        updated = None

        for row in rows:
            if row.get(PromoCSVFields.CODE) == normalized_code:
                current = int(row.get(PromoCSVFields.TIMES_USED, "0"))
                row[PromoCSVFields.TIMES_USED] = str(current + 1)
                updated = row
                break

        if updated is None:
            return None

        self._rewrite_all_rows(rows)
        return updated

    def _rewrite_all_rows(self, rows: List[Dict[str, str]]) -> None:
        """rewrites the csv file with the given rows (helper for update/delete)"""
        import csv
        with self._file_lock:
            with open(self.file_path, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)