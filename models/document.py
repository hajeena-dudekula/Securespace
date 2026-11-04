from extensions import db

class Document(db.Model):

    __tablename__ = "secure_documents"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    stored_filename = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        default="General"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("secure_accounts.id"),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )
