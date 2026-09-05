def get_auth_token(client, email="income_user@example.com"):
    client.post("/auth/register", json={
        "name": "Income User",
        "email": email,
        "password": "Password123"
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": "Password123"
    })
    return res.json()["access_token"]


def test_income_crud(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Create income
    income_payload = {
        "amount": 50000.0,
        "source": "Software Engineer Job",
        "category": "Salary",
        "date": "2026-09-01",
        "description": "Monthly salary"
    }
    create_res = client.post("/income", json=income_payload, headers=headers)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["amount"] == 50000.0
    assert created_data["source"] == "Software Engineer Job"
    income_id = created_data["id"]

    # 2. List incomes
    list_res = client.get("/income", headers=headers)
    assert list_res.status_code == 200
    items = list_res.json()
    assert len(items) >= 1
    assert any(item["id"] == income_id for item in items)

    # 3. Retrieve single income
    get_res = client.get(f"/income/{income_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == income_id

    # 4. Update income
    update_payload = {
        "amount": 55000.0,
        "source": "Senior Software Engineer Job"
    }
    update_res = client.put(f"/income/{income_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["amount"] == 55000.0
    assert update_res.json()["source"] == "Senior Software Engineer Job"

    # 5. Delete income
    del_res = client.delete(f"/income/{income_id}", headers=headers)
    assert del_res.status_code == 200

    # Verify deleted
    get_after_del = client.get(f"/income/{income_id}", headers=headers)
    assert get_after_del.status_code == 404

    # 6. Unauthorized access
    unauth_res = client.get("/income")
    assert unauth_res.status_code in [401, 403]
