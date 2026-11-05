import importlib.util
from pathlib import Path

import pytest

from extensions import db


PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_FILE = PROJECT_ROOT / "app.py"

spec = importlib.util.spec_from_file_location(
    "trustvault_test_app",
    APP_FILE
)
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)


@pytest.fixture
def app(tmp_path):
    database_path = tmp_path / "test_securespace.db"

    test_app = app_module.create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
        "SECRET_KEY": "test-secret-key",
        "WTF_CSRF_ENABLED": False,
    })

    test_app.instance_path = str(tmp_path / "instance")
    Path(test_app.instance_path).mkdir(parents=True, exist_ok=True)

    with test_app.app_context():
        db.drop_all()
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()



from werkzeug.security import generate_password_hash

from models.user import User
from models.document import Document


@pytest.fixture
def users(app):
    with app.app_context():
        owner = User(
            username="testowner",
            email="owner@test.local",
            password=generate_password_hash("OwnerPass123!"),
            role="owner"
        )

        viewer = User(
            username="testviewer",
            email="viewer@test.local",
            password=generate_password_hash("ViewerPass123!"),
            role="viewer"
        )

        db.session.add_all([owner, viewer])
        db.session.commit()

        return {
            "owner_id": owner.id,
            "viewer_id": viewer.id
        }


@pytest.fixture
def sample_document(app, users):
    import os

    with app.app_context():
        document = Document(
            filename="sample.txt",
            stored_filename="test-sample.txt",
            category="General",
            user_id=users["owner_id"]
        )

        db.session.add(document)
        db.session.commit()

        upload_folder = os.path.join(
            app.instance_path,
            "documents"
        )
        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(
            upload_folder,
            "test-sample.txt"
        )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Test document content")

        return document.id


@pytest.fixture
def login_as(client):
    def _login(username, password):
        return client.post(
            "/login",
            data={
                "username": username,
                "password": password
            },
            follow_redirects=True
        )

    return _login
