def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_index_serves_web_client(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_register_rejects_duplicate_username(client):
    body = {"username": "duplicate_user", "password": "s3cret-pass"}
    assert client.post("/register", json=body).status_code == 201
    assert client.post("/register", json=body).status_code == 400


def test_register_validates_input(client):
    assert client.post("/register", json={"username": "ab", "password": "s3cret-pass"}).status_code == 422
    assert client.post("/register", json={"username": "valid_name", "password": "short"}).status_code == 422


def test_login_rejects_wrong_password(client):
    client.post("/register", json={"username": "login_user", "password": "s3cret-pass"})
    response = client.post("/login", json={"username": "login_user", "password": "wrong-pass"})
    assert response.status_code == 401


def test_calculate_requires_token(client):
    assert client.post("/calculate", json={"expression": "1+1"}).status_code == 401


def test_calculate_and_history(client, auth_header):
    response = client.post("/calculate", json={"expression": "(2 + 3) * 4"}, headers=auth_header)
    assert response.status_code == 200
    assert response.json() == {"expression": "(2 + 3) * 4", "result": 20.0}

    client.post("/calculate", json={"expression": "10 / 4"}, headers=auth_header)
    history = client.get("/history", headers=auth_header).json()
    assert [row["expression"] for row in history] == ["10 / 4", "(2 + 3) * 4"]


def test_history_is_private_per_user(client, auth_header):
    client.post("/calculate", json={"expression": "7 * 6"}, headers=auth_header)
    client.post("/register", json={"username": "other_user", "password": "s3cret-pass"})
    other = client.post("/login", json={"username": "other_user", "password": "s3cret-pass"}).json()["access_token"]
    assert client.get("/history", headers={"Authorization": f"Bearer {other}"}).json() == []


def test_invalid_expression_returns_400(client, auth_header):
    for expr in ["2 +", "1 / 0", "__import__('os')", "True + 1"]:
        response = client.post("/calculate", json={"expression": expr}, headers=auth_header)
        assert response.status_code == 400, expr


def test_swagger_token_endpoint(client):
    client.post("/register", json={"username": "swagger_user", "password": "s3cret-pass"})
    response = client.post("/token", data={"username": "swagger_user", "password": "s3cret-pass"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
