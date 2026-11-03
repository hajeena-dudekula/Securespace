from datetime import datetime
from app import db


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(db.String(255), nullable=False)

    stored_filename = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        default="General"
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
