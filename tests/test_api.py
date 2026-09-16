import uuid
from decimal import Decimal
import pytest
from fastapi.testclient import TestClient

from main import app
from db import SessionLocal
from models import User, Transaction, Category

client = TestClient(app)


@pytest.fixture(scope="module")
def test_user():
    """Create a unique test user and return credentials + auth token."""
    unique_id = uuid.uuid4().hex[:8]
    username = f"test_{unique_id}"
    password = "TestPassword123!"

    # Register user
    reg_response = client.post(
        "/users/",
        json={"username": username, "password": password}
    )
    assert reg_response.status_code == 201
    user_data = reg_response.json()

    # Login user
    login_response = client.post(
        "/users/login",
        json={"username": username, "password": password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    yield {
        "id": user_data["id"],
        "username": username,
        "password": password,
        "token": token,
        "headers": headers,
    }

    # Teardown: delete test transactions and user
    db = SessionLocal()
    try:
        db.query(Transaction).filter(Transaction.user_id == user_data["id"]).delete()
        db.query(User).filter(User.id == user_data["id"]).delete()
        db.commit()
    finally:
        db.close()


def test_root_endpoint():
    """Verify root health endpoint returns 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Personal Finance API"}


def test_user_registration_duplicate():
    """Verify duplicate registration returns 409 Conflict."""
    unique_id = uuid.uuid4().hex[:8]
    username = f"dup_{unique_id}"
    password = "Password123"

    res1 = client.post("/users/", json={"username": username, "password": password})
    assert res1.status_code == 201

    res2 = client.post("/users/", json={"username": username, "password": password})
    assert res2.status_code == 409

    # Cleanup
    db = SessionLocal()
    try:
        db.query(User).filter(User.username == username).delete()
        db.commit()
    finally:
        db.close()


def test_user_login_invalid_credentials():
    """Verify login with invalid password returns 401."""
    response = client.post(
        "/users/login",
        json={"username": "nonexistent_user_xyz", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_unauthenticated_access_blocked():
    """Verify protected endpoints reject requests without a token."""
    response = client.get("/transactions/")
    assert response.status_code == 401

    response = client.get("/finance/summary")
    assert response.status_code == 401


def test_invalid_token_blocked():
    """Verify requests with malformed tokens return 401."""
    headers = {"Authorization": "Bearer completely-invalid-token"}
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 401


def test_transaction_crud_and_finance_summary(test_user):
    """End-to-end test of Transaction CRUD operations and Finance Summary calculation."""
    headers = test_user["headers"]

    # 1. Verify invalid category_id returns 400
    invalid_tx = {
        "amount": 50.00,
        "type": "expense",
        "category_id": 999999,
        "name": "Invalid Category Test",
        "description": "Should fail",
        "transaction_date": "2026-09-15"
    }
    res_invalid = client.post("/transactions/", json=invalid_tx, headers=headers)
    assert res_invalid.status_code == 400

    # 2. Create an Income Transaction (Category 8 = Salary)
    income_tx = {
        "amount": 5000.00,
        "type": "income",
        "category_id": 8,
        "name": "Monthly Salary",
        "description": "September paycheck",
        "transaction_date": "2026-09-01"
    }
    res_income = client.post("/transactions/", json=income_tx, headers=headers)
    assert res_income.status_code == 201
    income_data = res_income.json()
    assert income_data["name"] == "Monthly Salary"
    assert Decimal(str(income_data["amount"])) == Decimal("5000.00")
    salary_id = income_data["id"]

    # 3. Create an Expense Transaction (Category 1 = Food)
    expense_tx = {
        "amount": 150.50,
        "type": "expense",
        "category_id": 1,
        "name": "Groceries",
        "description": "Supermarket haul",
        "transaction_date": "2026-09-05"
    }
    res_expense = client.post("/transactions/", json=expense_tx, headers=headers)
    assert res_expense.status_code == 201
    expense_data = res_expense.json()
    groceries_id = expense_data["id"]

    # 4. Read single transaction
    res_get = client.get(f"/transactions/{groceries_id}", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json()["id"] == groceries_id
    assert res_get.json()["name"] == "Groceries"

    # 5. Read all transactions with filters
    res_list = client.get("/transactions/?transaction_type=expense", headers=headers)
    assert res_list.status_code == 200
    items = res_list.json()
    assert any(tx["id"] == groceries_id for tx in items)
    assert not any(tx["id"] == salary_id for tx in items)

    # 6. Full update (PUT)
    updated_expense = {
        "amount": 175.25,
        "type": "expense",
        "category_id": 1,
        "name": "Groceries & Supplies",
        "description": "Updated supermarket run",
        "transaction_date": "2026-09-05"
    }
    res_put = client.put(f"/transactions/{groceries_id}", json=updated_expense, headers=headers)
    assert res_put.status_code == 200
    assert res_put.json()["name"] == "Groceries & Supplies"
    assert Decimal(str(res_put.json()["amount"])) == Decimal("175.25")

    # 7. Partial update (PATCH)
    res_patch = client.patch(
        f"/transactions/{groceries_id}",
        json={"name": "Weekly Groceries"},
        headers=headers
    )
    assert res_patch.status_code == 200
    assert res_patch.json()["name"] == "Weekly Groceries"
    assert Decimal(str(res_patch.json()["amount"])) == Decimal("175.25")

    # 8. Check Finance Summary
    res_summary = client.get("/finance/summary", headers=headers)
    assert res_summary.status_code == 200
    summary = res_summary.json()
    expected_income = Decimal("5000.00")
    expected_expense = Decimal("175.25")
    expected_balance = expected_income - expected_expense
    assert Decimal(str(summary["total_income"])) == expected_income
    assert Decimal(str(summary["total_expenses"])) == expected_expense
    assert Decimal(str(summary["balance"])) == expected_balance

    # 9. Delete transaction
    res_delete = client.delete(f"/transactions/{groceries_id}", headers=headers)
    assert res_delete.status_code == 200

    # 10. Verify deleted transaction is not found (404)
    res_verify_del = client.get(f"/transactions/{groceries_id}", headers=headers)
    assert res_verify_del.status_code == 404


def test_transactions_validation_errors(test_user):
    """Verify 400 validation errors on transactions endpoint."""
    headers = test_user["headers"]

    # Invalid date range
    res = client.get("/transactions/?start_date=2026-09-10&end_date=2026-09-01", headers=headers)
    assert res.status_code == 400
    assert "start_date cannot be later than end_date" in res.json()["detail"]

    # Invalid amount range
    res = client.get("/transactions/?min_amount=100&max_amount=50", headers=headers)
    assert res.status_code == 400
    assert "min_amount cannot be greater than max_amount" in res.json()["detail"]

    # Finance summary invalid date range
    res = client.get("/finance/summary?start_date=2026-09-10&end_date=2026-09-01", headers=headers)
    assert res.status_code == 400
    assert "start_date cannot be later than end_date" in res.json()["detail"]

