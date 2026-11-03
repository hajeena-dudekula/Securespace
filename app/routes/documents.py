import os
import uuid

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import db
from app.models.document import Document


documents_bp = Blueprint(
    "documents",
    __name__,
    url_prefix="/documents"
)


ALLOWED_EXTENSIONS = {
    "pdf",
    "doc",
    "docx",
    "txt",
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@documents_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_document():

    if request.method == "POST":

        file = request.files.get("file")

        category = request.form.get(
            "category",
            "General"
        )

        if not file or file.filename == "":
            flash("Please select a file.")
            return redirect(url_for("documents.upload_document"))

        if not allowed_file(file.filename):
            flash("Invalid file type.")
            return redirect(url_for("documents.upload_document"))

        original_filename = secure_filename(file.filename)

        stored_filename = (
            str(uuid.uuid4())
            + "_"
            + original_filename
        )

        upload_folder = os.path.join(
            current_app.instance_path,
            "documents"
        )

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(
            upload_folder,
            stored_filename
        )

        file.save(file_path)

        document = Document(
            filename=original_filename,
            stored_filename=stored_filename,
            category=category,
            user_id=current_user.id
        )

        db.session.add(document)
        db.session.commit()

        flash("Document uploaded successfully!")

        return redirect(
            url_for("documents.list_documents")
        )

    return render_template("documents/upload.html")


@documents_bp.route("/")
@login_required
def list_documents():

    documents = Document.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Document.upload_date.desc()
    ).all()

    return render_template(
        "documents/list.html",
        documents=documents
    )
