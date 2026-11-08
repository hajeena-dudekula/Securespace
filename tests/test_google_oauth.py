from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from extensions import db


class FakeGoogleClient:
    def __init__(self, userinfo):
        self.userinfo_data = userinfo

    def authorize_access_token(self):
        return {"userinfo": self.userinfo_data}


def mock_google_client(monkeypatch, userinfo):
    from routes.auth import oauth

    fake_client = FakeGoogleClient(userinfo)

    monkeypatch.setattr(
        oauth,
        "create_client",
        lambda name: fake_client
    )


def test_google_login_creates_verified_viewer_account(
    client, app, monkeypatch
):
    mock_google_client(monkeypatch, {
        "email": "googleuser@gmail.com",
        "email_verified": True,
        "name": "Google User"
    })

    response = client.get("/login/google/callback")

    assert response.status_code == 302
    assert response.location.endswith("/dashboard")

    with app.app_context():
        account = User.query.filter_by(
            email="googleuser@gmail.com"
        ).first()

        assert account is not None
        assert account.role == "viewer"
        assert account.password != ""


def test_google_login_preserves_existing_account(
    client, app, monkeypatch
):
    with app.app_context():
        account = User(
            username="existinguser",
            email="existing@gmail.com",
            password=generate_password_hash("OriginalPass123!"),
            role="owner"
        )
        db.session.add(account)
        db.session.commit()
        original_password = account.password

    mock_google_client(monkeypatch, {
        "email": "existing@gmail.com",
        "email_verified": True
    })

    response = client.get("/login/google/callback")

    assert response.status_code == 302

    with app.app_context():
        account = User.query.filter_by(
            email="existing@gmail.com"
        ).first()

        assert account.role == "owner"
        assert account.password == original_password
        assert check_password_hash(
            account.password,
            "OriginalPass123!"
        )


def test_google_login_rejects_unverified_email(
    client, app, monkeypatch
):
    mock_google_client(monkeypatch, {
        "email": "unverified@gmail.com",
        "email_verified": False
    })

    response = client.get("/login/google/callback")

    assert response.status_code == 302
    assert response.location.endswith("/login")

    with app.app_context():
        account = User.query.filter_by(
            email="unverified@gmail.com"
        ).first()

        assert account is None


def test_google_login_handles_missing_credentials(client, app):
    app.config["GOOGLE_CLIENT_ID"] = None
    app.config["GOOGLE_CLIENT_SECRET"] = None

    response = client.get("/login/google")

    assert response.status_code == 302
    assert response.location.endswith("/login")
