import uuid


def _register_user(client, email: str, password: str = "StrongPassword123"):
    r = client.post("/auth/register", json={"email": email, "password": password})
    assert r.status_code == 201, r.text
    return r.json()


def _login_get_token(client, email: str, password: str = "StrongPassword123") -> str:
    r = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data, data
    return data["access_token"]


def test_users_me_requires_token(client):
    r = client.get("/users/me")
    assert r.status_code == 401, r.text


def test_users_me_with_token_returns_user(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123"

    _register_user(client, email, password)
    token = _login_get_token(client, email, password)

    r = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text

    data = r.json()
    assert data["email"] == email
    assert "id" in data


def test_patch_users_me_updates_email(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123"

    _register_user(client, email, password)
    token = _login_get_token(client, email, password)

    new_email = f"updated_{uuid.uuid4().hex[:8]}@example.com"
    r = client.patch(
        "/users/me",
        json={"email": new_email},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200, r.text

    data = r.json()
    assert data["email"] == new_email

    # Confirm it persists (GET /users/me returns updated email)
    r2 = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r2.status_code == 200, r2.text
    assert r2.json()["email"] == new_email
