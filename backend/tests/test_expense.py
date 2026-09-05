def get_auth_token(client, email="expense_user@example.com"):
    client.post("/auth/register", json={
        "name": "Expense User",
        "email": email,
        "password": "Password123"
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": "Password123"
    })
    return res.json()["access_token"]


def test_expense_crud(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Validation failure on amount <= 0
    bad_payload = {
        "amount": 0,
        "category": "Food",
        "date": "2026-09-02",
        "description": "Lunch"
    }
    bad_res = client.post("/expenses", json=bad_payload, headers=headers)
    assert bad_res.status_code == 422

    # 2. Create expense
    expense_payload = {
        "amount": 1200.0,
        "category": "Food",
        "date": "2026-09-02",
        "description": "Dinner with friends"
    }
    create_res = client.post("/expenses", json=expense_payload, headers=headers)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["amount"] == 1200.0
    assert created_data["category"] == "Food"
    expense_id = created_data["id"]

    # 3. List expenses
    list_res = client.get("/expenses", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(item["id"] == expense_id for item in items)

    # 4. Retrieve single expense
    get_res = client.get(f"/expenses/{expense_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == expense_id

    # 5. Update expense
    update_payload = {
        "amount": 1500.0,
        "description": "Dinner with family"
    }
    update_res = client.put(f"/expenses/{expense_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["amount"] == 1500.0
    assert update_res.json()["description"] == "Dinner with family"

    # 6. Delete expense
    del_res = client.delete(f"/expenses/{expense_id}", headers=headers)
    assert del_res.status_code == 200

    # 7. Verify deleted
    get_after_del = client.get(f"/expenses/{expense_id}", headers=headers)
    assert get_after_del.status_code == 404

    # 8. Unauthorized access
    unauth_res = client.get("/expenses")
    assert unauth_res.status_code in [401, 403]
