from extensions import db
from datetime import datetime, timezone


class AuditLog(db.Model):

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("secure_accounts.id"),
        nullable=True
    )

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("secure_documents.id"),
        nullable=True
    )

    action = db.Column(
        db.String(50),
        nullable=False
    )

    details = db.Column(
        db.Text,
        nullable=True
    )

    ip_address = db.Column(
        db.String(45),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )
