import uuid


def test_register_success(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {"email": email, "password": "StrongPassword123"}

    r = client.post("/auth/register", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["email"] == email
    assert "id" in data


def test_register_duplicate_email_returns_409(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123"

    r1 = client.post("/auth/register", json={"email": email, "password": password})
    assert r1.status_code == 201, r1.text

    r2 = client.post("/auth/register", json={"email": email, "password": password})
    assert r2.status_code == 409, r2.text


def test_login_success_returns_token(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123"

    # register
    r1 = client.post("/auth/register", json={"email": email, "password": password})
    assert r1.status_code == 201, r1.text

    # login (OAuth2PasswordRequestForm => x-www-form-urlencoded)
    r2 = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    if "expires_in" in data:
        assert isinstance(data["expires_in"], int)


def test_login_wrong_password_returns_401(client):
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPassword123"

    r1 = client.post("/auth/register", json={"email": email, "password": password})
    assert r1.status_code == 201, r1.text

    r2 = client.post(
        "/auth/login",
        data={"username": email, "password": "WrongPassword123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r2.status_code == 401, r2.text
