def get_auth_token(client, email="ai_user@example.com"):
    client.post("/auth/register", json={
        "name": "AI User",
        "email": email,
        "password": "Password123"
    })
    res = client.post("/auth/login", json={
        "email": email,
        "password": "Password123"
    })
    return res.json()["access_token"]


def test_ai_chat_and_history(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Ask a question
    payload = {"message": "What is compound interest?"}
    chat_res = client.post("/ai/chat", json=payload, headers=headers)
    assert chat_res.status_code == 201
    chat_data = chat_res.json()
    assert chat_data["user_message"] == "What is compound interest?"
    assert len(chat_data["ai_response"]) > 0
    chat_id = chat_data["id"]

    # 2. Retrieve history
    hist_res = client.get("/ai/history", headers=headers)
    assert hist_res.status_code == 200
    hist_items = hist_res.json()
    assert len(hist_items) >= 1
    assert any(h["id"] == chat_id for h in hist_items)

    # 3. Delete history item
    del_res = client.delete(f"/ai/history/{chat_id}", headers=headers)
    assert del_res.status_code == 200

    # 4. Verify history item is gone
    hist_after = client.get("/ai/history", headers=headers).json()
    assert not any(h["id"] == chat_id for h in hist_after)
