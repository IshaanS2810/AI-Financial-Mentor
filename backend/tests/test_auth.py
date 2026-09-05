def test_register_and_login(client):
    # 1. Register
    reg_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "Password123!"
    }
    res = client.post("/auth/register", json=reg_data)
    assert res.status_code == 200
    user_json = res.json()
    assert user_json["email"] == "testuser@example.com"
    assert user_json["name"] == "Test User"
    assert "password_hash" not in user_json

    # 2. Duplicate email
    res_dup = client.post("/auth/register", json=reg_data)
    assert res_dup.status_code == 400

    # 3. Login with wrong password
    res_bad = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "WrongPassword"
    })
    assert res_bad.status_code == 401

    # 4. Login with correct password
    res_login = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "password": "Password123!"
    })
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    token = token_data["access_token"]

    # 5. /auth/me without token
    res_no_auth = client.get("/auth/me")
    assert res_no_auth.status_code in [401, 403]

    # 6. /auth/me with valid token
    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/auth/me", headers=headers)
    assert res_me.status_code == 200
    me_json = res_me.json()
    assert me_json["email"] == "testuser@example.com"
    assert "password_hash" not in me_json
