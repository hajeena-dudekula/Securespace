import os

import pytest
from pypdf import PdfReader
from reportlab.pdfgen import canvas

from extensions import db
from models.document import Document
from models.permission import DocumentPermission
import routes.documents as documents_module


def storage_path(app, filename):
    return os.path.join(app.instance_path, "documents", filename)


def grant_permission(app, document_id, users, permission):
    with app.app_context():
        record = DocumentPermission(
            document_id=document_id,
            user_id=users["viewer_id"],
            permission=permission,
            granted_by=users["owner_id"]
        )
        db.session.add(record)
        db.session.commit()


def test_owner_can_open_and_save_txt(
    app, client, users, sample_document, login_as
):
    login_as("testowner", "OwnerPass123!")

    response = client.get(
        f"/documents/edit-content/{sample_document}"
    )
    assert response.status_code == 200
    assert b"Test document content" in response.data

    response = client.post(
        f"/documents/save-content/{sample_document}",
        data={"content": "Updated TXT content"}
    )
    assert response.status_code == 302

    with open(storage_path(app, "test-sample.txt"), encoding="utf-8") as file:
        assert file.read() == "Updated TXT content"


def test_shared_editor_can_save_txt(
    app, client, users, sample_document, login_as
):
    grant_permission(app, sample_document, users, "edit")
    login_as("testviewer", "ViewerPass123!")

    response = client.post(
        f"/documents/save-content/{sample_document}",
        data={"content": "Shared editor updated this"}
    )
    assert response.status_code == 302

    with open(storage_path(app, "test-sample.txt"), encoding="utf-8") as file:
        assert file.read() == "Shared editor updated this"


def test_viewer_cannot_open_or_save_txt(
    app, client, users, sample_document, login_as
):
    grant_permission(app, sample_document, users, "read")
    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/edit-content/{sample_document}"
    )
    assert response.status_code == 403

    response = client.post(
        f"/documents/save-content/{sample_document}",
        data={"content": "Unauthorized change"}
    )
    assert response.status_code == 403

    with open(storage_path(app, "test-sample.txt"), encoding="utf-8") as file:
        assert file.read() == "Test document content"


def test_owner_can_edit_pdf(app, client, users, login_as):
    with app.app_context():
        document = Document(
            filename="sample.pdf",
            stored_filename="test-sample.pdf",
            category="General",
            user_id=users["owner_id"]
        )
        db.session.add(document)
        db.session.commit()
        document_id = document.id

    pdf_path = storage_path(app, "test-sample.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    pdf = canvas.Canvas(pdf_path)
    pdf.drawString(72, 750, "Original PDF content")
    pdf.save()

    login_as("testowner", "OwnerPass123!")

    response = client.get(f"/documents/edit-content/{document_id}")
    assert response.status_code == 200
    assert b"Original PDF content" in response.data

    response = client.post(
        f"/documents/save-content/{document_id}",
        data={"content": "Updated PDF content"}
    )
    assert response.status_code == 302

    reader = PdfReader(pdf_path)
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "Updated PDF content" in extracted
    assert os.path.isfile(pdf_path + ".original.bak")


def test_failed_save_restores_original_txt(
    app, client, users, sample_document, login_as, monkeypatch
):
    login_as("testowner", "OwnerPass123!")

    def fail_audit(**kwargs):
        raise RuntimeError("Simulated audit failure")

    monkeypatch.setattr(
        documents_module,
        "create_signed_audit_log",
        fail_audit
    )

    response = client.post(
        f"/documents/save-content/{sample_document}",
        data={"content": "This change must be rolled back"}
    )

    assert response.status_code == 302

    with open(storage_path(app, "test-sample.txt"), encoding="utf-8") as file:
        assert file.read() == "Test document content"
