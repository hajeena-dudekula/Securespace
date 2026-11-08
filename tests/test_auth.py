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


def test_registration_creates_owner_account(client, app):
    from models.user import User

    response = client.post(
        "/register",
        data={
            "username": "newowner",
            "email": "newowner@test.local",
            "password": "OwnerPassword123!",
            "role": "owner"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        account = User.query.filter_by(username="newowner").first()
        assert account is not None
        assert account.role == "owner"


def test_registration_rejects_admin_role(client, app):
    from models.user import User

    response = client.post(
        "/register",
        data={
            "username": "fakeadmin",
            "email": "fakeadmin@test.local",
            "password": "AdminPassword123!",
            "role": "admin"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        account = User.query.filter_by(username="fakeadmin").first()
        assert account is None



def test_registration_rejects_weak_passwords(client, app):
    from models.user import User

    weak_passwords = [
        "short1!",
        "alllowercase123!",
        "ALLUPPERCASE123!",
        "NoNumbers!!",
        "NoSpecial123",
        "password123",
        "A" * 129
    ]

    for index, password in enumerate(weak_passwords):
        response = client.post(
            "/register",
            data={
                "username": f"weakuser{index}",
                "email": f"weakuser{index}@test.local",
                "password": password,
                "role": "viewer"
            },
            follow_redirects=True
        )

        assert response.status_code == 200

        with app.app_context():
            account = User.query.filter_by(
                username=f"weakuser{index}"
            ).first()
            assert account is None


def test_registration_accepts_strong_password(client, app):
    from models.user import User

    response = client.post(
        "/register",
        data={
            "username": "stronguser",
            "email": "stronguser@test.local",
            "password": "SecurePass123!@",
            "role": "viewer"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():
        account = User.query.filter_by(username="stronguser").first()
        assert account is not None
        assert account.password != "SecurePass123!@"

def test_login_remember_me_sets_persistent_cookie(client):
    client.post(
        "/register",
        data={
            "username": "rememberuser",
            "email": "remember@test.local",
            "password": "RememberPass123!",
            "role": "viewer"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "rememberuser",
            "password": "RememberPass123!",
            "remember": "on"
        }
    )

    cookies = response.headers.getlist("Set-Cookie")
    remember_cookie = next(
        (cookie for cookie in cookies if cookie.startswith("remember_token=")),
        None
    )

    assert response.status_code == 302
    assert remember_cookie is not None
    assert "Expires=" in remember_cookie


def test_login_without_remember_me_uses_session_cookie_only(client):
    client.post(
        "/register",
        data={
            "username": "sessionuser",
            "email": "session@test.local",
            "password": "SessionPass123!",
            "role": "viewer"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "sessionuser",
            "password": "SessionPass123!"
        }
    )

    cookies = response.headers.getlist("Set-Cookie")
    remember_cookie = [
        cookie for cookie in cookies
        if cookie.startswith("remember_token=")
    ]

    assert response.status_code == 302
    assert not remember_cookie

def test_forgot_password_shows_same_message_for_unknown_email(client):
    response = client.post(
        "/forgot-password",
        data={"email": "unknown@test.local"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"If an account exists" in response.data


def test_password_reset_updates_password_and_invalidates_old_token(client, app):
    from models.user import User
    from extensions import db
    from routes.auth import get_reset_serializer
    from werkzeug.security import check_password_hash

    client.post(
        "/register",
        data={
            "username": "resetuser",
            "email": "reset@test.local",
            "password": "OriginalPass123!",
            "role": "viewer"
        }
    )

    with app.app_context():
        account = User.query.filter_by(username="resetuser").first()
        token = get_reset_serializer().dumps({
            "user_id": account.id,
            "password_hash": account.password
        })

    response = client.post(
        f"/reset-password/{token}",
        data={"password": "NewSecurePass123!"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Password reset successful" in response.data

    with app.app_context():
        account = User.query.filter_by(username="resetuser").first()
        assert check_password_hash(account.password, "NewSecurePass123!")

    old_token_response = client.get(f"/reset-password/{token}")
    assert old_token_response.status_code == 302
    assert "/forgot-password" in old_token_response.location


def test_password_reset_rejects_invalid_token(client):
    response = client.get("/reset-password/invalid-token")

    assert response.status_code == 302
    assert "/forgot-password" in response.location


def test_password_reset_rejects_weak_new_password(client, app):
    from models.user import User
    from extensions import db
    from routes.auth import get_reset_serializer

    client.post(
        "/register",
        data={
            "username": "weakreset",
            "email": "weakreset@test.local",
            "password": "OriginalPass123!",
            "role": "viewer"
        }
    )

    with app.app_context():
        account = User.query.filter_by(username="weakreset").first()
        original_hash = account.password
        token = get_reset_serializer().dumps({
            "user_id": account.id,
            "password_hash": account.password
        })

    response = client.post(
        f"/reset-password/{token}",
        data={"password": "weak"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"at least 8 characters" in response.data

    with app.app_context():
        account = User.query.filter_by(username="weakreset").first()
        assert account.password == original_hash

