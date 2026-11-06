from datetime import datetime

from models.document import Document
from models.user import User
from extensions import db


def test_admin_can_filter_documents_by_owner(
    app, client, users, sample_document, login_as
):
    login_as("testowner", "OwnerPass123!")

    with app.app_context():
        admin = User(
            username="testadmin",
            email="admin@test.local",
            password=User.query.filter_by(
                id=users["owner_id"]
            ).first().password,
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

    client.post("/logout")
    login_as("testadmin", "OwnerPass123!")

    response = client.get("/documents/?owner=testowner")

    assert response.status_code == 200
    assert b"sample.txt" in response.data


def test_non_admin_cannot_filter_by_other_owner(
    client, users, sample_document, login_as
):
    login_as("testviewer", "ViewerPass123!")

    response = client.get("/documents/?owner=testowner")

    assert response.status_code == 200
    assert b"sample.txt" not in response.data


def test_date_filter_includes_document_on_selected_date(
    app, client, users, sample_document, login_as
):
    with app.app_context():
        document = db.session.get(Document, sample_document)
        document.uploaded_at = datetime(2026, 11, 6, 6, 0, 0)
        db.session.commit()

    login_as("testowner", "OwnerPass123!")

    response = client.get(
        "/documents/?date_from=2026-11-06&date_to=2026-11-06"
    )

    assert response.status_code == 200
    assert b"sample.txt" in response.data


def test_date_filter_excludes_document_outside_selected_date(
    app, client, users, sample_document, login_as
):
    with app.app_context():
        document = db.session.get(Document, sample_document)
        document.uploaded_at = datetime(2026, 11, 5, 6, 0, 0)
        db.session.commit()

    login_as("testowner", "OwnerPass123!")

    response = client.get(
        "/documents/?date_from=2026-11-06&date_to=2026-11-06"
    )

    assert response.status_code == 200
    assert b"sample.txt" not in response.data
