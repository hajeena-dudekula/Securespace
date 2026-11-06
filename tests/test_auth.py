def test_user_can_register_and_login(client):
    response = client.post(
        "/register",
        data={
            "username": "testowner",
            "email": "owner@test.local",
            "password": "TestPassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    response = client.post(
        "/login",
        data={
            "username": "testowner",
            "password": "TestPassword123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200


def test_login_rate_limit_blocks_sixth_attempt(client):
    for attempt in range(5):
        response = client.post(
            "/login",
            data={
                "username": "unknown_user",
                "password": "WrongPassword123!"
            },
            environ_overrides={"REMOTE_ADDR": "192.0.2.10"}
        )
        assert response.status_code == 200, f"Attempt {attempt + 1} failed"

    response = client.post(
        "/login",
        data={
            "username": "unknown_user",
            "password": "WrongPassword123!"
        },
        environ_overrides={"REMOTE_ADDR": "192.0.2.10"}
    )

    assert response.status_code == 429

def test_login_rate_limit(client):
    for _ in range(5):
        response = client.post(
            "/login",
            data={
                "username": "unknown_user",
                "password": "WrongPassword123!"
            },
            environ_base={"REMOTE_ADDR": "192.0.2.10"}
        )
        assert response.status_code == 200

    response = client.post(
        "/login",
        data={
            "username": "unknown_user",
            "password": "WrongPassword123!"
        },
        environ_base={"REMOTE_ADDR": "192.0.2.10"}
    )

    assert response.status_code == 429

def test_login_rejects_missing_csrf_token(client, app):
    app.config["WTF_CSRF_ENABLED"] = True

    response = client.post(
        "/login",
        data={
            "username": "unknown_user",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 400
