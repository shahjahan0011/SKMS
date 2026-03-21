"""Mock Payment Service Module"""
import uuid
from app.storage.repositories.order_repository import get_order_by_id
from app.storage.repositories.order_repository import get_order_by_id, update_order
from app.services.notification_service import notification_service

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

        expected_total = float(order.get("total", 0.0))

        if amount is not None:
            if float(amount) != expected_total:
                raise ValueError(f"Payment rejected: Amount {amount} does not match order total {expected_total}")

        payment_amount = float(amount) if amount is not None else expected_total

        if payment_amount >= 1000.00:
            result = {
                "transaction_id": None,
                "order_id": order_id,
                "amount_processed": payment_amount,
                "payment_status": "failed",
                "message": "Payment simulation failed: Transaction declined by bank (limit exceeded)."
            }

            try:
                notification_service().notify_payment_result(order["username"], order_id, False)
            except Exception:
                pass

            return result

        transaction_id = f"txn_{uuid.uuid4().hex[:12]}"

        update_order(order_id, {"status": "paid"})
        
        result = {
            "transaction_id": transaction_id,
            "order_id": order_id,
            "amount_processed": payment_amount,
            "payment_status": "success",
            "message": "Payment simulation successful."
        }

        try:
            notification_service().notify_payment_result(order["username"], order_id, True)
        except Exception:
            pass

        return result
    