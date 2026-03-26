# Testing Documents

This folder contains testing evidence for Milestone 3.

## Contents

- `coverage.xml`  
  XML coverage report generated from the full test suite.

- `coverage_summary.txt`  
  Terminal output from the pytest coverage run, showing overall test execution and coverage results.

- `coverage_html/`  
  HTML coverage report. Open `index.html` in this folder to view the full report.

- `pytest_terminal_pass.png`  
  Screenshot showing local `pytest` execution in the terminal with all tests passing.

- `github_actions_runs_overview.png`  
  Screenshots of the GitHub Actions workflow page showing successful CI runs.

- `github_actions_pytest_pass.png`  
  Screenshot of a successful GitHub Actions run showing the pytest job passed.

## Testing Included

The backend test suite includes unit tests, integration tests, and endpoint/API tests.

### Example Unit Test Files
- `test_auth_service.py`
- `test_notification_service.py`
- `test_order_service.py`
- `test_menu_service.py`
- `test_restaurant_service.py`
- `test_user_repository.py`
- `test_notification_repository.py`
- `test_base_csv_repository.py`
- `test_user_schema.py`

### Example Integration Test Files
- `test_dependencies.py`
- `test_csv_store.py`
- `test_menu_pagination.py`
- `test_authorization.py`

### Example Endpoint/API Test Files
- `test_auth_router.py`
- `test_notification_router.py`
- `test_order_router.py`
- `test_payment_router.py`
- `test_menu_router.py`
- `test_restaurant_router.py`
- `test_delivery_router.py`
- `test_item_listing_routers.py`

For unit testing, `monkeypatch` was used to isolate dependencies and mock behavior where needed.

## How to Open the HTML Coverage Report

### On macOS
From the project root, run:


open testing-documents/coverage_html/index.html

### On Windows 

From the project root, run:

start testing-documents\coverage_html\index.html