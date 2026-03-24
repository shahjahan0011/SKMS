import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

MOCK_PENDING_ORDER = {
    "order_id": "ord_123",
    "username": "jahan",
    "status": "pending",
    "total": "45.50"
}

MOCK_DELIVERED_ORDER = {
    "order_id": "ord_456",
    "username": "jahan",
    "status": "delivered",
    "total": "30.00"
}

MOCK_HIGH_VALUE_ORDER = {
    "order_id": "ord_999",
    "username": "jahan",
    "status": "pending",
    "total": "1500.00"
}

MOCK_ALREADY_PAID_ORDER = {
    "order_id": "ord_789",
    "username": "jahan",
    "status": "preparing",
    "total": "25.00"
}


@patch("app.services.payment_service.NotificationService")
@patch("app.services.payment_service.update_order")
@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_success_for_pending_order(mock_get_order, mock_update_order, mock_notification_service):
    """Test that a pending order successfully generates a transaction ID and updates the DB to 'paid'."""
    mock_get_order.return_value = MOCK_PENDING_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": 45.50}
    )

    assert response.status_code == 200
    data = response.json().get("data", {})

    assert data["payment_status"] == "success"
    assert "transaction_id" in data
    assert data["order_id"] == "ord_123"

    mock_update_order.assert_called_once()
    updated_order_arg = mock_update_order.call_args[0][0]
    assert updated_order_arg["order_id"] == "ord_123"
    assert updated_order_arg["status"] == "paid"

@patch("app.services.payment_service.NotificationService")
@patch("app.services.payment_service.update_order")
@patch("app.services.payment_service.get_order_by_id")
def test_initiate_payment_success_triggers_notification(mock_get_order, mock_update_order, mock_notification_service):
    """Test successful payment triggers customer notification."""
    mock_get_order.return_value = MOCK_PENDING_ORDER
    mock_notification_instance = mock_notification_service.return_value

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": 45.50}
    )

    assert response.status_code == 200
    mock_notification_instance.notify_payment_result.assert_called_once_with(
        "jahan",
        "ord_123",
        True
    )


@patch("app.services.payment_service.NotificationService")
@patch("app.services.payment_service.update_order")
@patch("app.services.payment_service.get_order_by_id")
def test_simulate_payment_failure_rule(mock_get_order, mock_update_order, mock_notification_service):
    """Test that a order breaking failure rule is unsuccessful and updates DB."""
    mock_get_order.return_value = MOCK_HIGH_VALUE_ORDER

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_999", "amount": 1500.00}
    )

    assert response.status_code == 200
    data = response.json().get("data", {})

    assert data["payment_status"] == "failed"
    assert "declined" in data["message"].lower()
    assert data["transaction_id"] is None

    mock_update_order.assert_called_once()

@patch("app.services.payment_service.NotificationService")
@patch("app.services.payment_service.update_order")
@patch("app.services.payment_service.get_order_by_id")
def test_simulate_payment_failure_triggers_notification(mock_get_order, mock_update_order, mock_notification_service):
    """Test failed payment triggers failure notification."""
    mock_get_order.return_value = MOCK_HIGH_VALUE_ORDER
    mock_notification_instance = mock_notification_service.return_value

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_999", "amount": 1500.00}
    )

    assert response.status_code == 200
    mock_notification_instance.notify_payment_result.assert_called_once_with(
        "jahan",
        "ord_999",
        False
    )


@pytest.mark.parametrize("test_amount, expected_status", [
    (0.01, "success"),
    (999.99, "success"),
    (1000.00, "failed"),
    (1000.01, "failed"),
])
@patch("app.services.payment_service.NotificationService")
@patch("app.services.payment_service.update_order")
@patch("app.services.payment_service.get_order_by_id")
def test_payment_amount_boundaries(mock_get_order, mock_update_order, mock_notification_service, test_amount, expected_status):
    """Test the exact penny boundaries of the simulated bank decline rule."""
    mock_get_order.return_value = {
        "order_id": "ord_boundary",
        "username": "jahan",
        "status": "pending",
        "total": str(test_amount)
    }

    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_boundary", "amount": test_amount}
    )

    assert response.status_code == 200
    data = response.json().get("data", {})
    assert data["payment_status"] == expected_status


@pytest.mark.parametrize("invalid_amount", [
    0.00,
    -0.01,
    -50.00,
])
def test_payment_invalid_amount_partitions(invalid_amount):
    """Test that zero or negative amounts are blocked immediately by validation partitions."""
    response = client.post(
        "/payments/initiate",
        json={"order_id": "ord_123", "amount": invalid_amount}
    )
    # FastAPI/Pydantic validation should block this before the service layer
    assert response.status_code == 422



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
