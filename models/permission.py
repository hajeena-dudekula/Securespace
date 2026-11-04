from extensions import db
from datetime import datetime, timezone


class DocumentPermission(db.Model):

    __tablename__ = "document_permissions"

    id = db.Column(db.Integer, primary_key=True)

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("secure_documents.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("secure_accounts.id"),
        nullable=False
    )

    permission = db.Column(
        db.String(20),
        nullable=False,
        default="read"
    )

    granted_by = db.Column(
        db.Integer,
        db.ForeignKey("secure_accounts.id"),
        nullable=False
    )

    granted_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "document_id",
            "user_id",
            name="unique_document_user_permission"
        ),
        db.CheckConstraint(
            "permission IN ('read', 'edit')",
            name="valid_document_permission"
        )
    )
