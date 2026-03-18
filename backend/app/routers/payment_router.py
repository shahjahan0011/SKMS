"""Payment routing module."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from app.services.payment_service import PaymentService

router = APIRouter()

class PaymentRequest(BaseModel):
    order_id: str = Field(..., description="The ID of the order being paid for")
    amount: float = Field(None, gt=0, description="The payment amount (optional validation)")

def get_payment_service():
    """Dependency injection for PaymentService."""
    return PaymentService()

@router.post("/payments/initiate", status_code=200)
def initiate_payment(
    request: PaymentRequest,
    service: PaymentService = Depends(get_payment_service)
):
    """
    Endpoint to initiate a payment.
    Will return 400 Bad Request if the order is not pending.
    """
    try:
        result = service.initiate_payment(
            order_id=request.order_id,
            amount=request.amount
        )
        return {"data": result}
    except ValueError as error:
        error_msg = str(error)
        if "not found" in error_msg.lower():
            raise HTTPException(status_code=404, detail=error_msg)

        raise HTTPException(status_code=400, detail=error_msg)
