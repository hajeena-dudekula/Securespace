from models.audit_log import AuditLog
from routes.documents import (
    create_signed_audit_log,
    verify_audit_chain
)


def test_empty_audit_chain_is_valid(app):
    with app.app_context():
        valid, failed_id = verify_audit_chain()

        assert valid is True
        assert failed_id is None


def test_signed_audit_events_verify_successfully(app):
    with app.app_context():
        create_signed_audit_log(
            actor_id=None,
            document_id=None,
            action="test_event_one",
            details="First test event",
            ip_address="127.0.0.1"
        )

        create_signed_audit_log(
            actor_id=None,
            document_id=None,
            action="test_event_two",
            details="Second test event",
            ip_address="127.0.0.1"
        )

        from extensions import db
        db.session.commit()

        valid, failed_id = verify_audit_chain()

        assert valid is True
        assert failed_id is None


def test_modified_audit_record_fails_verification(app):
    with app.app_context():
        audit = create_signed_audit_log(
            actor_id=None,
            document_id=None,
            action="test_event",
            details="Original details",
            ip_address="127.0.0.1"
        )

        from extensions import db
        db.session.commit()

        audit.details = "Modified details"
        db.session.commit()

        valid, failed_id = verify_audit_chain()

        assert valid is False
        assert failed_id == audit.id
