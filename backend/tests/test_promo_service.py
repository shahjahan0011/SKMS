"""Unit tests for promo service"""

import pytest
from app.services.promo_service import PromoService


class stub_promo_repository:
    """stub repository for promo service tests"""

    def __init__(self):
        self.promos = {}

    def promo_exists(self, code):
        return code.upper() in self.promos

    def get_promo_by_code(self, code):
        return self.promos.get(code.upper())

    def get_all_promos(self):
        return list(self.promos.values())

    def create_promo(self, code, discount_percent, max_uses):
        normalized = code.upper()
        promo = {
            "code": normalized,
            "discount_percent": str(discount_percent),
            "max_uses": str(max_uses),
            "times_used": "0",
            "active": "true",
            "created_at": "2026-01-01T00:00:00"
        }
        self.promos[normalized] = promo
        return promo

    def delete_promo(self, code):
        normalized = code.upper()
        if normalized in self.promos:
            del self.promos[normalized]
            return True
        return False

    def set_active_status(self, code, active):
        normalized = code.upper()
        if normalized not in self.promos:
            return None
        self.promos[normalized]["active"] = "true" if active else "false"
        return self.promos[normalized]

    def increment_times_used(self, code):
        normalized = code.upper()
        if normalized not in self.promos:
            return None
        current = int(self.promos[normalized]["times_used"])
        self.promos[normalized]["times_used"] = str(current + 1)
        return self.promos[normalized]


def make_service():
    service = PromoService()
    service.promo_repo = stub_promo_repository()
    return service


def test_create_promo_success():
    service = make_service()
    result = service.create_promo("SAVE10", 10, 0)
    assert result["code"] == "SAVE10"
    assert result["discount_percent"] == "10"
    assert result["times_used"] == "0"


def test_create_promo_normalizes_to_uppercase():
    service = make_service()
    result = service.create_promo("save20", 20, 0)
    assert result["code"] == "SAVE20"


def test_create_promo_empty_code_fails():
    service = make_service()
    with pytest.raises(ValueError):
        service.create_promo("", 10, 0)


def test_create_promo_invalid_discount_too_low():
    service = make_service()
    with pytest.raises(ValueError):
        service.create_promo("BAD", 0, 0)


def test_create_promo_invalid_discount_too_high():
    service = make_service()
    with pytest.raises(ValueError):
        service.create_promo("BAD", 101, 0)


def test_create_promo_duplicate_fails():
    service = make_service()
    service.create_promo("DUPE", 10, 0)
    with pytest.raises(ValueError):
        service.create_promo("DUPE", 15, 0)


def test_create_promo_negative_max_uses_fails():
    service = make_service()
    with pytest.raises(ValueError):
        service.create_promo("BAD", 10, -1)


def test_apply_promo_success():
    service = make_service()
    service.create_promo("SAVE10", 10, 0)
    result = service.apply_promo("SAVE10", 100.0)
    assert result["discount_amount"] == 10.0
    assert result["final_total"] == 90.0
    assert result["original_total"] == 100.0


def test_apply_promo_increments_usage():
    service = make_service()
    service.create_promo("SAVE10", 10, 5)
    service.apply_promo("SAVE10", 100.0)
    promo = service.get_promo("SAVE10")
    assert promo["times_used"] == "1"


def test_apply_promo_not_found():
    service = make_service()
    with pytest.raises(ValueError):
        service.apply_promo("NOPE", 100.0)


def test_apply_promo_inactive_fails():
    service = make_service()
    service.create_promo("OFF", 10, 0)
    service.toggle_promo_active("OFF", False)
    with pytest.raises(ValueError):
        service.apply_promo("OFF", 100.0)


def test_apply_promo_usage_limit_reached():
    service = make_service()
    service.create_promo("LIMIT", 10, 1)
    service.apply_promo("LIMIT", 100.0)
    with pytest.raises(ValueError):
        service.apply_promo("LIMIT", 100.0)


def test_apply_promo_unlimited_uses():
    service = make_service()
    service.create_promo("UNLIMITED", 10, 0)
    for _ in range(5):
        result = service.apply_promo("UNLIMITED", 100.0)
        assert result["final_total"] == 90.0


def test_apply_promo_zero_total_fails():
    service = make_service()
    service.create_promo("SAVE10", 10, 0)
    with pytest.raises(ValueError):
        service.apply_promo("SAVE10", 0)


def test_apply_promo_negative_total_fails():
    service = make_service()
    service.create_promo("SAVE10", 10, 0)
    with pytest.raises(ValueError):
        service.apply_promo("SAVE10", -50)


def test_delete_promo_success():
    service = make_service()
    service.create_promo("BYE", 10, 0)
    result = service.delete_promo("BYE")
    assert "deleted" in result["message"]


def test_delete_promo_not_found():
    service = make_service()
    with pytest.raises(ValueError):
        service.delete_promo("GHOST")


def test_toggle_promo_active():
    service = make_service()
    service.create_promo("TOGGLE", 10, 0)
    result = service.toggle_promo_active("TOGGLE", False)
    assert result["active"] == "false"


def test_get_all_promos():
    service = make_service()
    service.create_promo("ONE", 10, 0)
    service.create_promo("TWO", 20, 0)
    promos = service.get_all_promos()
    assert len(promos) == 2


def test_full_discount_100_percent():
    service = make_service()
    service.create_promo("FREE", 100, 0)
    result = service.apply_promo("FREE", 50.0)
    assert result["final_total"] == 0.0
    assert result["discount_amount"] == 50.0