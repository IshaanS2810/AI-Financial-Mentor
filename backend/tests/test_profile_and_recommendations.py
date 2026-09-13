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


def test_scenario_no_income(client):
    token = register_and_login(client, "No Income User", "no_income@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # User has 20,000 in expenses but 0 income
    client.post("/expenses", json={
        "amount": 20000.0,
        "category": "Food",
        "date": "2026-09-01",
        "description": "Groceries"
    }, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    summary = res.json()["financial_summary"]
    assert summary["monthly_income"] == 0.0
    assert summary["monthly_expenses"] == 20000.0
    assert summary["monthly_savings"] == -20000.0
    assert summary["savings_rate"] == 0.0
    assert summary["investment_readiness"] == "NOT_READY"
    assert summary["investment_capacity"] == 0.0

    # Verify rec_cashflow_stabilization is generated with HIGH priority
    recs = res.json()["recommendations"]
    rec_cashflow = next((r for r in recs if r["id"] == "rec_cashflow_stabilization"), None)
    assert rec_cashflow is not None
    assert rec_cashflow["priority"] == "HIGH"

    # AI Mentor check
    res_ai = client.post("/ai/chat", json={"message": "Can I afford to invest right now?"}, headers=headers)
    assert res_ai.status_code in [200, 201]
    reply = res_ai.json()["ai_response"]
    assert "no recorded income" in reply.lower() or "not ready" in reply.lower() or "deficit" in reply.lower()


def test_scenario_no_expenses(client):
    token = register_and_login(client, "No Expense User", "no_expenses@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # User earns 50,000 but has not recorded any expenses yet
    client.post("/income", json={
        "amount": 50000.0,
        "source": "Salary",
        "category": "Salary",
        "date": "2026-09-01"
    }, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    summary = res.json()["financial_summary"]
    assert summary["monthly_income"] == 50000.0
    assert summary["monthly_expenses"] == 0.0
    assert summary["monthly_savings"] == 50000.0
    assert summary["savings_rate"] == 100.0
    # Because emergency fund is 0, readiness asks to build emergency fund
    assert summary["investment_readiness"] == "BUILD_EMERGENCY_FUND"
    assert summary["investment_capacity"] > 0


def test_scenario_expenses_greater_than_income(client):
    token = register_and_login(client, "Deficit User", "deficit@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Earns 30,000, spends 45,000
    client.post("/income", json={
        "amount": 30000.0,
        "source": "Stipend",
        "category": "Salary",
        "date": "2026-09-01"
    }, headers=headers)
    client.post("/expenses", json={
        "amount": 45000.0,
        "category": "Shopping",
        "date": "2026-09-02",
        "description": "Electronics"
    }, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    summary = res.json()["financial_summary"]
    assert summary["monthly_income"] == 30000.0
    assert summary["monthly_expenses"] == 45000.0
    assert summary["monthly_savings"] == -15000.0
    assert summary["savings_rate"] == 0.0  # Clamped to 0.0, not negative!
    assert summary["investment_readiness"] == "NOT_READY"
    assert summary["investment_capacity"] == 0.0

    recs = res.json()["recommendations"]
    rec_cashflow = next((r for r in recs if r["id"] == "rec_cashflow_stabilization"), None)
    assert rec_cashflow is not None
    assert rec_cashflow["priority"] == "HIGH"


def test_scenario_high_savings(client):
    token = register_and_login(client, "High Saver", "high_saver@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Setup profile with 6+ months emergency reserve
    client.post("/profile", json={
        "age": 30,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 200000.0
    }, headers=headers)

    # Incomes 100,000, Expenses 20,000 -> 80% savings rate, 10 months emergency runway
    client.post("/income", json={
        "amount": 100000.0,
        "source": "Tech Job",
        "category": "Salary",
        "date": "2026-09-01"
    }, headers=headers)
    client.post("/expenses", json={
        "amount": 20000.0,
        "category": "Rent",
        "date": "2026-09-02",
        "description": "Apartment rent"
    }, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    summary = res.json()["financial_summary"]
    assert summary["monthly_savings"] == 80000.0
    assert summary["savings_rate"] == 80.0
    assert summary["estimated_emergency_months"] == 10.0
    assert summary["investment_readiness"] == "STRONG_INVESTMENT_CAPACITY"
    # Capacity is 80% of surplus (64,000)
    assert summary["investment_capacity"] == 64000.0

    # Verify equity SIP is recommended with HIGH priority
    recs = res.json()["recommendations"]
    rec_sip = next((r for r in recs if r["id"] == "rec_long_term_sip_equity"), None)
    assert rec_sip is not None
    assert rec_sip["priority"] == "HIGH"


def test_scenario_missing_financial_profile(client):
    token = register_and_login(client, "No Profile User", "no_profile@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/income", json={
        "amount": 40000.0,
        "source": "Salary",
        "category": "Salary",
        "date": "2026-09-01"
    }, headers=headers)

    # Recommendations endpoint should succeed even without profile configured
    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    rec_data = res.json()
    assert rec_data["profile"] is None
    assert rec_data["financial_summary"]["monthly_income"] == 40000.0
    assert len(rec_data["recommendations"]) > 0

    # AI Chat handles missing profile gracefully without crashing
    res_ai = client.post("/ai/chat", json={"message": "Can I afford to invest?"}, headers=headers)
    assert res_ai.status_code in [200, 201]
    assert "Financial Profile" in res_ai.json()["ai_response"]


def test_scenario_insufficient_emergency_fund(client):
    token = register_and_login(client, "Low Emergency User", "low_em@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/profile", json={
        "age": 27,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 5000.0  # Only 5,000 saved
    }, headers=headers)

    client.post("/income", json={"amount": 50000.0, "source": "Salary", "category": "Salary", "date": "2026-09-01"}, headers=headers)
    client.post("/expenses", json={"amount": 25000.0, "category": "Bills", "date": "2026-09-02", "description": "Utilities"}, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    summary = res.json()["financial_summary"]
    # 5,000 / 25,000 = 0.2 months coverage
    assert summary["estimated_emergency_months"] == 0.2
    assert summary["investment_readiness"] == "BUILD_EMERGENCY_FUND"

    # Emergency fund priority is HIGH
    recs = res.json()["recommendations"]
    rec_em = next((r for r in recs if r["id"] == "rec_emergency_fund_priority"), None)
    assert rec_em is not None
    assert rec_em["priority"] == "HIGH"

    # AI query about emergency fund
    res_ai = client.post("/ai/chat", json={"message": "Should I focus on my emergency fund first?"}, headers=headers)
    assert res_ai.status_code in [200, 201]
    assert "Yes, absolutely!" in res_ai.json()["ai_response"]


def test_scenario_conservative_short_term_investor(client):
    token = register_and_login(client, "Conservative User", "conservative_short@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/profile", json={
        "age": 40,
        "risk_tolerance": "Conservative",
        "investment_horizon": "Less than 3 years",
        "financial_goal": "Short-term savings",
        "emergency_fund": 150000.0
    }, headers=headers)

    client.post("/income", json={"amount": 60000.0, "source": "Salary", "category": "Salary", "date": "2026-09-01"}, headers=headers)
    client.post("/expenses", json={"amount": 20000.0, "category": "Bills", "date": "2026-09-02", "description": "Needs"}, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    recs = res.json()["recommendations"]

    # Must recommend short-term capital preservation
    rec_short = next((r for r in recs if r["id"] == "rec_short_term_capital_preservation"), None)
    assert rec_short is not None
    assert rec_short["priority"] == "HIGH"
    assert "Fixed Deposits" in rec_short["suggested_action"] or "Debt Funds" in rec_short["suggested_action"]

    # Must NOT recommend volatile long-term equity SIP
    rec_equity = next((r for r in recs if r["id"] == "rec_long_term_sip_equity"), None)
    assert rec_equity is None


def test_scenario_moderate_risk_long_term_investor(client):
    token = register_and_login(client, "Moderate Long User", "mod_long@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/profile", json={
        "age": 26,
        "risk_tolerance": "Moderate",
        "investment_horizon": "More than 10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 100000.0
    }, headers=headers)

    client.post("/income", json={"amount": 50000.0, "source": "Salary", "category": "Salary", "date": "2026-09-01"}, headers=headers)
    client.post("/expenses", json={"amount": 20000.0, "category": "Food", "date": "2026-09-02", "description": "Needs"}, headers=headers)

    res = client.get("/recommendations", headers=headers)
    assert res.status_code == 200
    recs = res.json()["recommendations"]

    # Must recommend long-term equity index SIP
    rec_sip = next((r for r in recs if r["id"] == "rec_long_term_sip_equity"), None)
    assert rec_sip is not None
    assert rec_sip["priority"] == "HIGH"
    assert "index mutual fund" in rec_sip["suggested_action"].lower()


def test_scenario_generic_and_personalized_ai_questions(client):
    token = register_and_login(client, "AI Query User", "ai_query@example.com", "Password123")
    headers = {"Authorization": f"Bearer {token}"}

    # Setup user data
    client.post("/profile", json={
        "age": 29,
        "risk_tolerance": "Moderate",
        "investment_horizon": "5–10 years",
        "financial_goal": "Wealth creation",
        "emergency_fund": 50000.0
    }, headers=headers)
    client.post("/income", json={"amount": 80000.0, "source": "Salary", "category": "Salary", "date": "2026-09-01"}, headers=headers)
    client.post("/expenses", json={"amount": 30000.0, "category": "Food", "date": "2026-09-02", "description": "Food"}, headers=headers)

    # 1. Generic Financial Concepts (knowledge base queries)
    res_generic1 = client.post("/ai/chat", json={"message": "What is compound interest?"}, headers=headers)
    assert res_generic1.status_code in [200, 201]
    assert "Compound Interest" in res_generic1.json()["ai_response"]

    res_generic2 = client.post("/ai/chat", json={"message": "What are mutual funds and how do they work?"}, headers=headers)
    assert res_generic2.status_code in [200, 201]
    assert "Mutual Fund" in res_generic2.json()["ai_response"]

    # 2. Personalized Financial Inquiries
    res_pers1 = client.post("/ai/chat", json={"message": "Can I afford to invest right now?"}, headers=headers)
    assert res_pers1.status_code in [200, 201]
    reply1 = res_pers1.json()["ai_response"]
    # Should cite their actual surplus or readiness
    assert "50,000" in reply1 or "80,000" in reply1 or "Surplus" in reply1

    res_pers2 = client.post("/ai/chat", json={"message": "How much should I invest every month?"}, headers=headers)
    assert res_pers2.status_code in [200, 201]
    reply2 = res_pers2.json()["ai_response"]
    assert "Recommended Monthly Investment Allocation" in reply2


def test_strict_multi_user_data_isolation_extended(client):
    """Deep isolation test verifying User B never sees User A's profile, recommendations, or AI context."""
    token_a = register_and_login(client, "Isolation User A", "iso_a@example.com", "Password123")
    token_b = register_and_login(client, "Isolation User B", "iso_b@example.com", "Password123")
    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # User A creates rich financial data
    client.post("/profile", json={
        "age": 45,
        "risk_tolerance": "Aggressive",
        "investment_horizon": "More than 10 years",
        "financial_goal": "Retirement",
        "emergency_fund": 750000.0
    }, headers=headers_a)
    client.post("/income", json={"amount": 350000.0, "source": "Consulting", "category": "Freelance", "date": "2026-09-01"}, headers=headers_a)
    client.post("/expenses", json={"amount": 80000.0, "category": "Shopping", "date": "2026-09-02", "description": "Luxury"}, headers=headers_a)

    # User B logs in fresh
    res_b_profile = client.get("/profile", headers=headers_b)
    assert res_b_profile.json() is None

    res_b_rec = client.get("/recommendations", headers=headers_b)
    b_summary = res_b_rec.json()["financial_summary"]
    # User B must see 0 values, never User A's 350,000 or 750,000
    assert b_summary["monthly_income"] == 0.0
    assert b_summary["monthly_expenses"] == 0.0
    assert b_summary["emergency_fund"] == 0.0
    assert b_summary["investment_readiness"] == "NOT_READY"

    # User B asks AI "How much can I invest?"
    res_b_ai = client.post("/ai/chat", json={"message": "How much should I invest every month?"}, headers=headers_b)
    assert res_b_ai.status_code in [200, 201]
    b_ai_text = res_b_ai.json()["ai_response"]
    # Must NOT mention User A's 350,000 or 750,000
    assert "350,000" not in b_ai_text
    assert "750,000" not in b_ai_text
