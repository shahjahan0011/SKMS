from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

MOCK_PENDING_ORDER = {
    "order_id": "ord_123",
    "status": "pending",
    "total": "45.50"
}

MOCK_DELIVERED_ORDER = {
    "order_id": "ord_456",
    "status": "delivered",
    "total": "30.00"
}

MOCK_ALREADY_PAID_ORDER = {
    "order_id": "ord_789",
    "status": "preparing",
    "total": "25.00"
}



@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_success_for_pending_order(mock_get_order):
    """Test that a pending order successfully generates a transaction ID."""
    mock_get_order.return_value = MOCK_PENDING_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": 45.50}
    )

    assert response.status_code == 200
    data = response.json().get("data", {})

    assert data["payment_status"] == "initiated"
    assert "transaction_id" in data
    assert data["order_id"] == "ord_123"


@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_rejects_non_pending_order(mock_get_order):
    """Test that a non-pending order (e.g., delivered) returns a generic 400."""
    mock_get_order.return_value = MOCK_DELIVERED_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_456", "amount": 30.00}
    )

    assert response.status_code == 400
    assert "Payment rejected" in response.json()["detail"]


@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_fails_if_already_paid(mock_get_order):
    """Test that an order marked with an 'already paid' status returns a specific 400."""
    mock_get_order.return_value = MOCK_ALREADY_PAID_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_789", "amount": 25.00}
    )

    assert response.status_code == 400
    assert "already been paid" in response.json()["detail"]


@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_order_not_found(mock_get_order):
    """Test that requesting payment for a non-existent order returns a 404."""
    mock_get_order.return_value = None

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_ghost", "amount": 10.00}
    )

    assert response.status_code == 404
    assert "Order not found" in response.json()["detail"]


@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_amount_mismatch_rejected(mock_get_order):
    """Test that an incorrect payment amount is rejected."""
    mock_get_order.return_value = MOCK_PENDING_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": 10.00}
    )

    assert response.status_code == 400
    assert "does not match order total" in response.json()["detail"]


def test_initiate_payment_negative_amount_blocked():
    """Test that our 'gt=0' Pydantic rule instantly blocks negative numbers."""
    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": -5.00}
    )

    assert response.status_code == 422
