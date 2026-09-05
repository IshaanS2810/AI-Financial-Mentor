def get_auth_token(client, email="dash_user@example.com"):
    client.post("/auth/register", json={
        "name": "Dashboard User",
        "email": email,
        "password": "Password123"
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": "Password123"
    })
    return res.json()["access_token"]


def test_dashboard_analytics(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Add income: 60,000 in 2026-08, 40,000 in 2026-09
    client.post("/income", json={
        "amount": 60000.0,
        "source": "Salary",
        "category": "Salary",
        "date": "2026-08-15"
    }, headers=headers)

    client.post("/income", json={
        "amount": 40000.0,
        "source": "Bonus",
        "category": "Bonus",
        "date": "2026-09-01"
    }, headers=headers)

    # Add expenses: 10,000 Food in 2026-08, 20,000 Rent in 2026-09
    client.post("/expenses", json={
        "amount": 10000.0,
        "category": "Food",
        "date": "2026-08-20",
        "description": "Groceries"
    }, headers=headers)

    client.post("/expenses", json={
        "amount": 20000.0,
        "category": "Bills",
        "date": "2026-09-02",
        "description": "Electricity & Rent"
    }, headers=headers)

    # 1. Test Summary
    summary_res = client.get("/dashboard/summary", headers=headers)
    assert summary_res.status_code == 200
    s_data = summary_res.json()
    assert s_data["total_income"] == 100000.0
    assert s_data["total_expenses"] == 30000.0
    assert s_data["savings"] == 70000.0

    # 2. Test Category Breakdown
    cat_res = client.get("/dashboard/category-breakdown", headers=headers)
    assert cat_res.status_code == 200
    c_data = cat_res.json()
    assert len(c_data) == 2
    cats = {item["category"]: item for item in c_data}
    assert "Bills" in cats
    assert cats["Bills"]["amount"] == 20000.0
    assert "Food" in cats
    assert cats["Food"]["amount"] == 10000.0

    # 3. Test Monthly Trend
    trend_res = client.get("/dashboard/monthly-trend", headers=headers)
    assert trend_res.status_code == 200
    t_data = trend_res.json()
    months = {item["month"]: item for item in t_data}
    assert "2026-08" in months
    assert months["2026-08"]["income"] == 60000.0
    assert months["2026-08"]["expenses"] == 10000.0
    assert months["2026-08"]["savings"] == 50000.0

    assert "2026-09" in months
    assert months["2026-09"]["income"] == 40000.0
    assert months["2026-09"]["expenses"] == 20000.0
    assert months["2026-09"]["savings"] == 20000.0
