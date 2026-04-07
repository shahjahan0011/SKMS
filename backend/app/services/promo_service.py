"""Business logic for promo codes"""

from typing import List, Dict, Optional

from app.storage.repositories.promo_repository import PromoRepository
from app.constants import PromoCSVFields, PromoErrorMessages


class PromoService:
    """service responsible for promo code business logic"""

    def __init__(self, promo_repo: PromoRepository = None):
        """Initialize promo service with optional repository injection"""
        self.promo_repo = promo_repo if promo_repo else PromoRepository()

    def create_promo(self, code: str, discount_percent: int, max_uses: int = 0) -> Dict:
        """create a new promo code with validation"""

        if not code or not code.strip():
            raise ValueError(PromoErrorMessages.CODE_REQUIRED)

        if discount_percent < 1 or discount_percent > 100:
            raise ValueError(PromoErrorMessages.INVALID_DISCOUNT)

        if max_uses < 0:
            raise ValueError(PromoErrorMessages.INVALID_MAX_USES)

        if self.promo_repo.promo_exists(code):
            raise ValueError(PromoErrorMessages.CODE_EXISTS)

        return self.promo_repo.create_promo(code.strip(), discount_percent, max_uses)

    def get_all_promos(self) -> List[Dict]:
        """return all promo codes"""
        return self.promo_repo.get_all_promos()

    def get_promo(self, code: str) -> Dict:
        """return one promo code by its code"""
        promo = self.promo_repo.get_promo_by_code(code)
        if promo is None:
            raise ValueError(PromoErrorMessages.CODE_NOT_FOUND)
        return promo

    def delete_promo(self, code: str) -> Dict:
        """delete a promo code"""
        deleted = self.promo_repo.delete_promo(code)
        if not deleted:
            raise ValueError(PromoErrorMessages.CODE_NOT_FOUND)
        return {"message": f"promo code {code.upper()} deleted"}

    def toggle_promo_active(self, code: str, active: bool) -> Dict:
        """activate or deactivate a promo code"""
        updated = self.promo_repo.set_active_status(code, active)
        if updated is None:
            raise ValueError(PromoErrorMessages.CODE_NOT_FOUND)
        return updated

    def apply_promo(self, code: str, order_total: float) -> Dict:
        """validate a promo code and calculate the discount for an order total"""

        if order_total <= 0:
            raise ValueError(PromoErrorMessages.INVALID_ORDER_TOTAL)

        promo = self.promo_repo.get_promo_by_code(code)
        if promo is None:
            raise ValueError(PromoErrorMessages.CODE_NOT_FOUND)

        if promo[PromoCSVFields.ACTIVE].lower() != "true":
            raise ValueError(PromoErrorMessages.CODE_INACTIVE)

        max_uses = int(promo[PromoCSVFields.MAX_USES])
        times_used = int(promo[PromoCSVFields.TIMES_USED])

        if max_uses > 0 and times_used >= max_uses:
            raise ValueError(PromoErrorMessages.CODE_USAGE_LIMIT_REACHED)

        discount_percent = int(promo[PromoCSVFields.DISCOUNT_PERCENT])
        discount_amount = round(order_total * (discount_percent / 100), 2)
        final_total = round(order_total - discount_amount, 2)

        self.promo_repo.increment_times_used(code)

        return {
            "code": promo[PromoCSVFields.CODE],
            "discount_percent": discount_percent,
            "original_total": round(order_total, 2),
            "discount_amount": discount_amount,
            "final_total": final_total
        }