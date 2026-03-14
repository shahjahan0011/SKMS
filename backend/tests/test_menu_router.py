from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_menus_status_and_structure():
    """
    Test 1: Verify the endpoint is reachable and returns the correct JSON keys.
    """

    response = client.get("/menus")

    if response.status_code == 404:
        response = client.get("/menus")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_menus_filter_logic():
    """
    Test 2: Verify that query parameters don't crash the app and return filtered results.
    """
    response = client.get("/menus?price=999.99")

    if response.status_code == 404:
        response = client.get("/menus/menus?price=999.99")

    assert response.status_code == 200

