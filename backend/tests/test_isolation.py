def register_and_login(client, name, email, password):
    client.post("/auth/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": password
    })
    return res.json()["access_token"]


def test_user_data_isolation(client):
    # Setup User A and User B
    token_a = register_and_login(client, "User A", "usera@example.com", "PasswordA123")
    token_b = register_and_login(client, "User B", "userb@example.com", "PasswordB123")

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 1. User A creates an Income record
    income_res = client.post("/income", json={
        "amount": 75000.0,
        "source": "Consulting A",
        "category": "Freelance",
        "date": "2026-09-01",
        "description": "User A exclusive income"
    }, headers=headers_a)
    assert income_res.status_code == 201
    income_a_id = income_res.json()["id"]

    # 2. User A creates an Expense record
    expense_res = client.post("/expenses", json={
        "amount": 12000.0,
        "category": "Shopping",
        "date": "2026-09-02",
        "description": "User A exclusive expense"
    }, headers=headers_a)
    assert expense_res.status_code == 201
    expense_a_id = expense_res.json()["id"]

    # 3. User A chats with AI
    chat_res = client.post("/ai/chat", json={
        "message": "User A private financial question"
    }, headers=headers_a)
    assert chat_res.status_code == 201
    chat_a_id = chat_res.json()["id"]

    # --- VERIFY USER B CANNOT ACCESS USER A's DATA ---

    # Income Isolation:
    # User B tries to GET User A's income
    get_inc = client.get(f"/income/{income_a_id}", headers=headers_b)
    assert get_inc.status_code == 404, "User B must not be able to retrieve User A's income"

    # User B tries to PUT User A's income
    put_inc = client.put(f"/income/{income_a_id}", json={"amount": 99999.0}, headers=headers_b)
    assert put_inc.status_code == 404, "User B must not be able to update User A's income"

    # User B tries to DELETE User A's income
    del_inc = client.delete(f"/income/{income_a_id}", headers=headers_b)
    assert del_inc.status_code == 404, "User B must not be able to delete User A's income"

    # User B listing income should be empty
    list_inc = client.get("/income", headers=headers_b)
    assert list_inc.status_code == 200
    assert not any(item["id"] == income_a_id for item in list_inc.json())

    # Expense Isolation:
    # User B tries to GET User A's expense
    get_exp = client.get(f"/expenses/{expense_a_id}", headers=headers_b)
    assert get_exp.status_code == 404, "User B must not be able to retrieve User A's expense"

    # User B tries to PUT User A's expense
    put_exp = client.put(f"/expenses/{expense_a_id}", json={"amount": 99999.0}, headers=headers_b)
    assert put_exp.status_code == 404, "User B must not be able to update User A's expense"

    # User B tries to DELETE User A's expense
    del_exp = client.delete(f"/expenses/{expense_a_id}", headers=headers_b)
    assert del_exp.status_code == 404, "User B must not be able to delete User A's expense"

    # User B listing expenses should be empty
    list_exp = client.get("/expenses", headers=headers_b)
    assert list_exp.status_code == 200
    assert not any(item["id"] == expense_a_id for item in list_exp.json())

    # Chat History Isolation:
    # User B listing chat history should not see User A's chat
    list_chat = client.get("/ai/history", headers=headers_b)
    assert list_chat.status_code == 200
    assert not any(item["id"] == chat_a_id for item in list_chat.json())

    # User B tries to DELETE User A's chat history item
    del_chat = client.delete(f"/ai/history/{chat_a_id}", headers=headers_b)
    assert del_chat.status_code == 404, "User B must not be able to delete User A's chat history"

    # Dashboard Isolation:
    # User B's dashboard must reflect 0 income, 0 expense, 0 savings
    dash_summary = client.get("/dashboard/summary", headers=headers_b)
    assert dash_summary.status_code == 200
    b_summary = dash_summary.json()
    assert b_summary["total_income"] == 0.0
    assert b_summary["total_expenses"] == 0.0
    assert b_summary["savings"] == 0.0
