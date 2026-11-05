from extensions import db
from models.permission import DocumentPermission
from models.audit_log import AuditLog
from models.document import Document


def test_owner_can_share_document_with_viewer(
    app, client, users, sample_document, login_as
):
    login_as("testowner", "OwnerPass123!")

    response = client.post(
        f"/documents/share/{sample_document}",
        data={"username": "testviewer", "permission": "read"}
    )

    assert response.status_code == 302

    with app.app_context():
        permission = DocumentPermission.query.filter_by(
            document_id=sample_document,
            user_id=users["viewer_id"]
        ).first()

        assert permission is not None
        assert permission.permission == "read"

        audit = AuditLog.query.filter_by(
            action="permission_granted",
            document_id=sample_document
        ).first()

        assert audit is not None


def test_owner_can_revoke_viewer_access(
    app, client, users, sample_document, login_as
):
    login_as("testowner", "OwnerPass123!")

    client.post(
        f"/documents/share/{sample_document}",
        data={"username": "testviewer", "permission": "read"}
    )

    response = client.post(
        f"/documents/revoke/{sample_document}",
        data={"username": "testviewer"}
    )

    assert response.status_code == 302

    with app.app_context():
        permission = DocumentPermission.query.filter_by(
            document_id=sample_document,
            user_id=users["viewer_id"]
        ).first()

        assert permission is None

        audit = AuditLog.query.filter_by(
            action="permission_revoked",
            document_id=sample_document
        ).first()

        assert audit is not None


def test_viewer_cannot_share_another_users_document(
    app, client, users, sample_document, login_as
):
    login_as("testviewer", "ViewerPass123!")

    response = client.post(
        f"/documents/share/{sample_document}",
        data={"username": "testowner", "permission": "edit"}
    )

    assert response.status_code == 404

    with app.app_context():
        permission = DocumentPermission.query.filter_by(
            document_id=sample_document,
            user_id=users["viewer_id"]
        ).first()

        assert permission is None

        audit = AuditLog.query.filter_by(
            action="permission_granted",
            document_id=sample_document
        ).first()

        assert audit is None


def test_viewer_with_read_permission_cannot_edit_document(
    app, client, users, sample_document, login_as
):
    with app.app_context():
        permission = DocumentPermission(
            document_id=sample_document,
            user_id=users["viewer_id"],
            granted_by=users["owner_id"],
            permission="read"
        )
        db.session.add(permission)
        db.session.commit()

    login_as("testviewer", "ViewerPass123!")

    response = client.post(
        f"/documents/edit/{sample_document}",
        data={"category": "Finance"}
    )

    assert response.status_code == 403

    with app.app_context():
        document = db.session.get(Document, sample_document)
        assert document.category == "General"


def test_viewer_cannot_delete_another_users_document(
    app, client, users, sample_document, login_as
):
    from models.document import Document

    login_as("testviewer", "ViewerPass123!")

    response = client.post(
        f"/documents/delete/{sample_document}"
    )

    assert response.status_code == 403

    with app.app_context():
        document = db.session.get(Document, sample_document)
        assert document is not None

def test_revoked_viewer_cannot_download_document(
    app, client, users, sample_document, login_as
):
    login_as("testowner", "OwnerPass123!")

    client.post(
        f"/documents/share/{sample_document}",
        data={"username": "testviewer", "permission": "read"}
    )

    client.post(
        f"/documents/revoke/{sample_document}",
        data={"username": "testviewer"}
    )

    client.get("/logout")

    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/download/{sample_document}"
    )

    assert response.status_code == 403

def test_unauthenticated_user_cannot_download_document(
    client, sample_document
):
    response = client.get(
        f"/documents/download/{sample_document}"
    )

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]

def test_viewer_with_read_permission_can_download_document(
    app, client, users, sample_document, login_as
):
    with app.app_context():
        permission = DocumentPermission(
            document_id=sample_document,
            user_id=users["viewer_id"],
            granted_by=users["owner_id"],
            permission="read"
        )
        db.session.add(permission)
        db.session.commit()

    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/download/{sample_document}"
    )

    assert response.status_code == 200
    assert response.data == b"Test document content"

def test_viewer_with_edit_permission_can_edit_document(
    app, client, users, sample_document, login_as
):
    with app.app_context():
        permission = DocumentPermission(
            document_id=sample_document,
            user_id=users["viewer_id"],
            granted_by=users["owner_id"],
            permission="edit"
        )
        db.session.add(permission)
        db.session.commit()

    login_as("testviewer", "ViewerPass123!")

    response = client.post(
        f"/documents/edit/{sample_document}",
        data={"category": "Finance"}
    )

    assert response.status_code == 302

    with app.app_context():
        document = db.session.get(Document, sample_document)
        assert document.category == "Finance"

        audit = AuditLog.query.filter_by(
            action="document_modified",
            document_id=sample_document
        ).first()

        assert audit is not None

def test_viewer_without_permission_cannot_preview_document(
    client, sample_document, login_as
):
    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/preview/{sample_document}"
    )

    assert response.status_code == 403

def test_admin_can_download_another_users_document(
    app, client, sample_document
):
    from werkzeug.security import generate_password_hash
    from models.user import User

    with app.app_context():
        admin = User(
            username="testadmin",
            email="admin@test.local",
            password=generate_password_hash("AdminPass123!"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "AdminPass123!"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    response = client.get(
        f"/documents/download/{sample_document}"
    )

    assert response.status_code == 200
    assert response.data == b"Test document content"

def test_admin_can_delete_another_users_document(
    app, client, sample_document
):
    from werkzeug.security import generate_password_hash
    from models.user import User
    from models.document import Document

    with app.app_context():
        admin = User(
            username="testadmin",
            email="admin@test.local",
            password=generate_password_hash("AdminPass123!"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "AdminPass123!"
        },
        follow_redirects=True
    )

    response = client.post(
        f"/documents/delete/{sample_document}"
    )

    assert response.status_code == 302

    with app.app_context():
        document = db.session.get(Document, sample_document)
        assert document is None

        audit = AuditLog.query.filter_by(
            action="document_deleted"
        ).first()

        assert audit is not None

def test_admin_can_edit_another_users_document(
    app, client, sample_document
):
    from werkzeug.security import generate_password_hash
    from models.user import User
    from models.document import Document

    with app.app_context():
        admin = User(
            username="testadmin",
            email="admin@test.local",
            password=generate_password_hash("AdminPass123!"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "AdminPass123!"
        },
        follow_redirects=True
    )

    response = client.post(
        f"/documents/edit/{sample_document}",
        data={"category": "Finance"}
    )

    assert response.status_code == 302

    with app.app_context():
        document = db.session.get(Document, sample_document)
        assert document.category == "Finance"

        audit = AuditLog.query.filter_by(
            action="document_modified",
            document_id=sample_document
        ).first()

        assert audit is not None

def test_viewer_cannot_access_admin_activity(client, users, login_as):
    login_as("testviewer", "ViewerPass123!")

    response = client.get("/admin/activity")

    assert response.status_code == 403


def test_admin_can_access_admin_activity(client, app):
    from werkzeug.security import generate_password_hash
    from models.user import User
    from extensions import db

    with app.app_context():
        admin = User(
            username="testadmin",
            email="admin@test.local",
            password=generate_password_hash("AdminPass123!"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

    client.post(
        "/login",
        data={
            "username": "testadmin",
            "password": "AdminPass123!"
        },
        follow_redirects=True
    )

    response = client.get("/admin/activity")

    assert response.status_code == 200

def test_denied_preview_attempt_is_logged(
    app, client, sample_document, login_as
):
    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/preview/{sample_document}"
    )

    assert response.status_code == 403

    with app.app_context():
        audit = AuditLog.query.filter_by(
            action="access_denied_preview"
        ).first()

        assert audit is not None
        assert audit.actor_id is not None


def test_denied_download_attempt_is_logged(
    app, client, sample_document, login_as
):
    login_as("testviewer", "ViewerPass123!")

    response = client.get(
        f"/documents/download/{sample_document}"
    )

    assert response.status_code == 403

    with app.app_context():
        audit = AuditLog.query.filter_by(
            action="access_denied_download"
        ).first()

        assert audit is not None
        assert audit.actor_id is not None
