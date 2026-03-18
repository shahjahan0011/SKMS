"""Mock Payment Service Module"""
import uuid
from app.storage.repositories.order_repository import get_order_by_id

class PaymentService:
    """Service for handling simulated payments."""

    def initiate_payment(self, order_id: str, amount: float = None) -> dict:
        """
        Initiates a payment attempt for an order.
        Enforces that orders must be in a 'pending' state.
        """
        order = get_order_by_id(order_id)

        if not order:
            raise ValueError("Order not found")

        current_status = str(order.get("status", "")).lower()
        already_paid_statuses = ["paid", "preparing", "in-transit", "delivered"]
        if current_status in already_paid_statuses:
            raise ValueError(f"Payment rejected: Order has already been paid (Status: {current_status}).")

        if current_status != "pending":
            raise ValueError(
                f"Payment rejected: Order is currently '{current_status}'. "
                "Payments can only be initiated for 'pending' orders."
            )

        if amount is not None:
            expected_total = float(order.get("total", 0.0))
            if float(amount) != expected_total:
                raise ValueError(f"Payment rejected: Amount {amount} does not match order total {expected_total}")

        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"

        return {
            "transaction_id": transaction_id,
            "order_id": order_id,
            "payment_status": "initiated",
            "message": "Payment attempt successfully initiated and acknowledged."
        }
