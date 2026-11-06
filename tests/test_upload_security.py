import io

from models.document import Document


def test_upload_accepts_matching_pdf_signature(client, app, users, login_as):
    login_as("testowner", "OwnerPass123!")

    response = client.post(
        "/documents/upload",
        data={
            "category": "General",
            "file": (
                io.BytesIO(b"%PDF-1.4\nTest PDF content"),
                "sample.pdf"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 302

    with app.app_context():
        assert Document.query.filter_by(filename="sample.pdf").count() == 1


def test_upload_rejects_fake_pdf_file(client, app, users, login_as):
    login_as("testowner", "OwnerPass123!")

    response = client.post(
        "/documents/upload",
        data={
            "category": "General",
            "file": (
                io.BytesIO(b"This is not a PDF file"),
                "fake.pdf"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 302

    with app.app_context():
        assert Document.query.filter_by(filename="fake.pdf").count() == 0


import zipfile
import pytest
from routes.documents import validate_file_content


def create_valid_docx():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("word/document.xml", "<document></document>")
    return buffer.getvalue()


@pytest.mark.parametrize("extension,valid_content,invalid_content", [
    ("png", b"\x89PNG\r\n\x1a\n" + b"test", b"not a PNG"),
    ("jpg", b"\xff\xd8\xff" + b"test", b"not a JPEG"),
    ("docx", create_valid_docx(), b"not a DOCX"),
    ("txt", b"SecureSpace test document", b"\\x00binary"),
])
def test_content_validation_for_supported_file_types(
    tmp_path, extension, valid_content, invalid_content
):
    valid_file = tmp_path / f"valid.{extension}"
    invalid_file = tmp_path / f"invalid.{extension}"

    valid_file.write_bytes(valid_content)
    invalid_file.write_bytes(invalid_content)

    assert validate_file_content(str(valid_file), extension) is True
    assert validate_file_content(str(invalid_file), extension) is False


def test_upload_sanitizes_path_traversal_filename(client, app, users, login_as):
    login_as("testowner", "OwnerPass123!")

    response = client.post(
        "/documents/upload",
        data={
            "category": "General",
            "file": (
                io.BytesIO(b"Safe text content"),
                "../../evil.txt"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 302

    with app.app_context():
        document = Document.query.filter_by(user_id=users["owner_id"]).filter_by(
            filename="evil.txt"
        ).first()

        assert document is not None
        assert "/" not in document.filename
        assert "\\" not in document.filename


def test_uploaded_file_is_stored_in_private_folder(
    client, app, users, login_as
):
    login_as("testowner", "OwnerPass123!")

    client.post(
        "/documents/upload",
        data={
            "category": "General",
            "file": (
                io.BytesIO(b"Private document content"),
                "private.txt"
            )
        },
        content_type="multipart/form-data"
    )

    with app.app_context():
        document = Document.query.filter_by(
            filename="private.txt",
            user_id=users["owner_id"]
        ).first()

        assert document is not None

        storage_folder = app.config.get("DOCUMENT_STORAGE_PATH")
        if not storage_folder:
            storage_folder = app.instance_path + "/documents"

        import os
        stored_path = os.path.join(storage_folder, document.stored_filename)

        assert os.path.isfile(stored_path)
        assert os.path.commonpath([
            os.path.abspath(storage_folder),
            os.path.abspath(stored_path)
        ]) == os.path.abspath(storage_folder)


def test_uploaded_file_is_not_publicly_accessible(
    client, app, users, login_as
):
    login_as("testowner", "OwnerPass123!")

    client.post(
        "/documents/upload",
        data={
            "category": "General",
            "file": (
                io.BytesIO(b"Private content"),
                "secret.txt"
            )
        },
        content_type="multipart/form-data"
    )

    with app.app_context():
        document = Document.query.filter_by(
            filename="secret.txt",
            user_id=users["owner_id"]
        ).first()

        assert document is not None
        response = client.get(
            f"/static/{document.stored_filename}"
        )
        assert response.status_code == 404
