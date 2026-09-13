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


def test_financial_profile_crud(client):
    token = register_and_login(client, "Profile Tester", "profile_test@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Initial GET profile should return null (empty)
    res_get = client.get("/profile", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json() is None

    # 2. Validation error on negative emergency fund
    bad_payload = {
        "age": 25,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": -5000.0
    }
    res_bad = client.post("/profile", json=bad_payload, headers=headers)
    assert res_bad.status_code == 422

    # 3. Create profile
    valid_payload = {
        "age": 24,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 75000.0,
        "risk_behavior": "Continue investing"
    }
    res_create = client.post("/profile", json=valid_payload, headers=headers)
    assert res_create.status_code == 200
    data = res_create.json()
    assert data["age"] == 24
    assert data["emergency_fund"] == 75000.0
    assert data["risk_tolerance"] == "Moderate"

    # 4. Update existing profile (upsert)
    update_payload = {
        "age": 25,
        "risk_tolerance": "Aggressive",
        "investment_horizon": "More than 10 years",
        "financial_goal": "Retirement",
        "emergency_fund": 90000.0,
        "risk_behavior": "Invest more"
    }
    res_update = client.post("/profile", json=update_payload, headers=headers)
    assert res_update.status_code == 200
    data_up = res_update.json()
    assert data_up["age"] == 25
    assert data_up["risk_tolerance"] == "Aggressive"
    assert data_up["emergency_fund"] == 90000.0

    # 5. GET profile returns updated record
    res_final = client.get("/profile", headers=headers)
    assert res_final.status_code == 200
    assert res_final.json()["risk_tolerance"] == "Aggressive"


def test_recommendations_and_readiness(client):
    token = register_and_login(client, "Rec Tester", "rec_test@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Setup profile: Emergency fund 30,000
    client.post("/profile", json={
        "age": 28,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 30000.0,
        "risk_behavior": "Continue investing"
    }, headers=headers)

    # Add Income: 60,000
    client.post("/income", json={
        "amount": 60000.0,
        "source": "Salary",
        "category": "Salary",
        "date": "2026-09-01"
    }, headers=headers)

    # Add Expenses: 30,000 (Food: 18,000, Transport: 12,000)
    client.post("/expenses", json={
        "amount": 18000.0,
        "category": "Food",
        "date": "2026-09-02",
        "description": "Dining and Groceries"
    }, headers=headers)
    client.post("/expenses", json={
        "amount": 12000.0,
        "category": "Transport",
        "date": "2026-09-03",
        "description": "Fuel"
    }, headers=headers)

    # Fetch Recommendations
    res_rec = client.get("/recommendations", headers=headers)
    assert res_rec.status_code == 200
    rec_data = res_rec.json()

    # Verify Financial Summary calculations
    summary = rec_data["financial_summary"]
    assert summary["monthly_income"] == 60000.0
    assert summary["monthly_expenses"] == 30000.0
    assert summary["monthly_savings"] == 30000.0
    assert summary["savings_rate"] == 50.0
    assert summary["emergency_fund"] == 30000.0
    # 30,000 / 30,000 = 1.0 month of emergency coverage
    assert summary["estimated_emergency_months"] == 1.0
    assert summary["investment_readiness"] == "BUILD_EMERGENCY_FUND"
    assert summary["investment_capacity"] > 0

    # Verify Recommendations list
    recs = rec_data["recommendations"]
    assert len(recs) >= 2
    # Emergency fund should be HIGH priority because coverage is 1 month (< 3 months)
    rec_em = next((r for r in recs if r["category"] == "EMERGENCY_FUND"), None)
    assert rec_em is not None
    assert rec_em["priority"] == "HIGH"


def test_user_isolation_for_profile_and_recommendations(client):
    token_a = register_and_login(client, "User A", "user_a_profile@example.com", "Password123")
    token_b = register_and_login(client, "User B", "user_b_profile@example.com", "Password123")

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates a profile and high income
    client.post("/profile", json={
        "age": 35,
        "risk_tolerance": "Aggressive",
        "investment_horizon": "More than 10 years",
        "financial_goal": "Retirement",
        "emergency_fund": 500000.0
    }, headers=headers_a)

    client.post("/income", json={
        "amount": 200000.0,
        "source": "Consulting",
        "category": "Freelance",
        "date": "2026-09-01"
    }, headers=headers_a)

    # User B checks their profile - should be None
    res_b_profile = client.get("/profile", headers=headers_b)
    assert res_b_profile.status_code == 200
    assert res_b_profile.json() is None

    # User B checks recommendations - should not see User A's data (income should be 0)
    res_b_rec = client.get("/recommendations", headers=headers_b)
    assert res_b_rec.status_code == 200
    b_summary = res_b_rec.json()["financial_summary"]
    assert b_summary["monthly_income"] == 0.0
    assert b_summary["emergency_fund"] == 0.0
