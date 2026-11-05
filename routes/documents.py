import os
import uuid

from datetime import datetime, timezone, timedelta


from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app,
    send_from_directory
)

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from extensions import db
from models.document import Document
from models.permission import DocumentPermission
from models.user import User
from models.audit_log import AuditLog

documents = Blueprint("documents", __name__, url_prefix="/documents")

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "png", "jpg", "jpeg"}

ALLOWED_CATEGORIES = {
    "General", "Personal", "Work", "Education", "Finance"
}

MAX_FILE_SIZES = {
    "pdf": 500 * 1024 * 1024,
    "docx": 100 * 1024 * 1024,
    "txt": 10 * 1024 * 1024,
    "png": 50 * 1024 * 1024,
    "jpg": 50 * 1024 * 1024,
    "jpeg": 50 * 1024 * 1024
}


def get_document_access(document_id):

    document = Document.query.get_or_404(document_id)

    if current_user.role == "admin":
        return document, "edit"

    if document.user_id == current_user.id:
        return document, "edit"

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=current_user.id
    ).first()

    if permission:
        return document, permission.permission

    return None, None

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@documents.route("/")
@login_required
def document_list():

    search = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()

    if current_user.role == "admin":
        query = Document.query
    else:
        query = Document.query.outerjoin(
            DocumentPermission,
            Document.id == DocumentPermission.document_id
        ).filter(
            or_(
                Document.user_id == current_user.id,
                DocumentPermission.user_id == current_user.id
            )
        ).distinct()

    if search:
        query = query.filter(Document.filename.ilike(f"%{search}%"))

    if category in ALLOWED_CATEGORIES:
        query = query.filter(Document.category == category)

    files = query.order_by(Document.uploaded_at.desc()).all()

    display_dates = {}

    for item in files:
        if item.uploaded_at:
            utc_time = item.uploaded_at.replace(tzinfo=timezone.utc)
            display_dates[item.id] = utc_time.astimezone(
                timezone(timedelta(hours=5, minutes=30))
            )

    access_levels = {}

    for item in files:
        if current_user.role == "admin" or item.user_id == current_user.id:
            access_levels[item.id] = "edit"
        else:
            permission = DocumentPermission.query.filter_by(
                document_id=item.id,
                user_id=current_user.id
            ).first()

            access_levels[item.id] = (
                permission.permission if permission else None
            )

    return render_template(
        "documents/list.html",
        files=files,
        search=search,
        category=category,
        display_dates=display_dates,
        access_levels=access_levels
    )


@documents.route("/upload", methods=["GET", "POST"])
@login_required
def upload_document():

    if request.method == "POST":

        file = request.files.get("file")
        category = request.form.get("category", "General")

        if not file or not file.filename:
            flash("Please select a file.", "error")
            return redirect(url_for("documents.upload_document"))

        safe_name = secure_filename(file.filename)

        if not safe_name or not allowed_file(safe_name):
            flash("File type is not allowed.", "error")
            return redirect(url_for("documents.upload_document"))

        if category not in ALLOWED_CATEGORIES:
            category = "General"

        extension = safe_name.rsplit(".", 1)[1].lower()
        stored_name = f"{uuid.uuid4().hex}.{extension}"

        upload_folder = os.path.join(
            current_app.instance_path,
            "documents"
        )

        os.makedirs(upload_folder, exist_ok=True)

        file_path = os.path.join(upload_folder, stored_name)

        try:
            file.save(file_path)

            file_size = os.path.getsize(file_path)
            max_size = MAX_FILE_SIZES[extension]

            if file_size > max_size:
                os.remove(file_path)
                flash(
                    f"File exceeds the {max_size // (1024 * 1024)} MB limit for this file type.",
                    "error"
                )
                return redirect(url_for("documents.upload_document"))

            document = Document(
                filename=safe_name,
                stored_filename=stored_name,
                category=category,
                user_id=current_user.id,
                uploaded_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )

            db.session.add(document)
            db.session.flush()

            db.session.add(AuditLog(
                actor_id=current_user.id,
                document_id=document.id,
                action="document_uploaded",
                details=f"Uploaded {safe_name}",
                ip_address=request.remote_addr
            ))

            db.session.commit()

            flash("Document uploaded successfully.", "success")
            return redirect(url_for("documents.document_list"))

        except Exception:
            db.session.rollback()

            if os.path.exists(file_path):
                os.remove(file_path)

            flash("Upload failed. Please try again.", "error")

    return render_template("documents/upload.html")


@documents.route("/preview/<int:document_id>")
@login_required
def preview_document(document_id):

    document, access = get_document_access(document_id)

    if not document or access not in {"read", "edit"}:

        db.session.add(AuditLog(
            actor_id=current_user.id,
            document_id=document.id if document else None,
            action="access_denied_preview",
            details=f"Unauthorized preview attempt for document ID {document_id}",
            ip_address=request.remote_addr
        ))
        db.session.commit()

        return "Access denied", 403

    extension = document.filename.rsplit(".", 1)[-1].lower()

    if extension not in {"pdf", "png", "jpg", "jpeg", "txt"}:
        flash("Preview is not supported for this file type.", "error")
        return redirect(url_for("documents.document_list"))

    upload_folder = os.path.join(
        current_app.instance_path,
        "documents"
    )

    db.session.add(AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action="document_previewed",
        details=f"Previewed {document.filename}",
        ip_address=request.remote_addr
    ))
    db.session.commit()

    return send_from_directory(
        upload_folder,
        document.stored_filename,
        as_attachment=False,
        download_name=document.filename
    )

@documents.route("/download/<int:document_id>")
@login_required
def download_document(document_id):

    document, access = get_document_access(document_id)

    if not document or access not in {"read", "edit"}:

        db.session.add(AuditLog(
            actor_id=current_user.id,
            document_id=document.id if document else None,
            action="access_denied_download",
            details=f"Unauthorized download attempt for document ID {document_id}",
            ip_address=request.remote_addr
        ))
        db.session.commit()

        return "Access denied", 403

    upload_folder = os.path.join(
        current_app.instance_path,
        "documents"
    )

    db.session.add(AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action="document_downloaded",
        details=f"Downloaded {document.filename}",
        ip_address=request.remote_addr
    ))
    db.session.commit()

    return send_from_directory(
        upload_folder,
        document.stored_filename,
        as_attachment=True,
        download_name=document.filename
    )





@documents.route("/share/<int:document_id>", methods=["POST"])
@login_required
def share_document(document_id):

    document = Document.query.filter_by(
        id=document_id,
        user_id=current_user.id
    ).first_or_404()

    username = request.form.get("username", "").strip()
    permission_type = request.form.get("permission", "read").strip()

    if permission_type not in {"read", "edit"}:
        flash("Invalid permission type.", "error")
        return redirect(url_for("documents.document_list"))

    target_user = User.query.filter_by(username=username).first()

    if not target_user:
        flash("User not found.", "error")
        return redirect(url_for("documents.document_list"))

    if target_user.id == current_user.id:
        flash("You already own this document.", "error")
        return redirect(url_for("documents.document_list"))

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=target_user.id
    ).first()

    if permission:
        permission.permission = permission_type
        permission.granted_by = current_user.id
    else:
        permission = DocumentPermission(
            document_id=document.id,
            user_id=target_user.id,
            permission=permission_type,
            granted_by=current_user.id
        )
        db.session.add(permission)

    db.session.add(AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action="permission_granted",
        details=f"{permission_type} access granted to {username}",
        ip_address=request.remote_addr
    ))

    db.session.commit()

    flash("Document access granted successfully.", "success")
    return redirect(url_for("documents.document_list"))

@documents.route("/revoke/<int:document_id>", methods=["POST"])
@login_required
def revoke_document_access(document_id):

    document = Document.query.filter_by(
        id=document_id,
        user_id=current_user.id
    ).first_or_404()

    username = request.form.get("username", "").strip()

    target_user = User.query.filter_by(username=username).first()

    if not target_user:
        flash("User not found.", "error")
        return redirect(url_for("documents.document_list"))

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=target_user.id
    ).first()

    if not permission:
        flash("No shared access found for this user.", "error")
        return redirect(url_for("documents.document_list"))

    db.session.add(AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action="permission_revoked",
        details=f"Access revoked from {username}",
        ip_address=request.remote_addr
    ))

    db.session.delete(permission)
    db.session.commit()

    flash("Document access revoked successfully.", "success")
    return redirect(url_for("documents.document_list"))




@documents.route("/edit/<int:document_id>", methods=["POST"])
@login_required
def edit_document(document_id):

    document, access = get_document_access(document_id)

    if not document or access != "edit":
        return "Access denied", 403

    category = request.form.get("category", "").strip()

    if category not in ALLOWED_CATEGORIES:
        flash("Invalid document category.", "error")
        return redirect(url_for("documents.document_list"))

    old_category = document.category
    document.category = category

    db.session.add(AuditLog(
        actor_id=current_user.id,
        document_id=document.id,
        action="document_modified",
        details=f"Category changed from {old_category} to {category}",
        ip_address=request.remote_addr
    ))

    db.session.commit()

    flash("Document updated successfully.", "success")
    return redirect(url_for("documents.document_list"))

@documents.route("/delete/<int:document_id>", methods=["POST"])
@login_required
def delete_document(document_id):

    document = Document.query.filter_by(
        id=document_id
    ).first_or_404()

    if current_user.role != "admin" and document.user_id != current_user.id:
        return "Access denied", 403

    upload_folder = os.path.join(
        current_app.instance_path,
        "documents"
    )

    file_path = os.path.join(
        upload_folder,
        document.stored_filename
    )

    try:
        db.session.add(AuditLog(
            actor_id=current_user.id,
            document_id=None,
            action="document_deleted",
            details=f"Deleted document ID {document.id}: {document.filename}",
            ip_address=request.remote_addr
        ))

        db.session.delete(document)
        db.session.commit()

        if os.path.exists(file_path):
            os.remove(file_path)

        flash("Document deleted successfully.", "success")

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Document deletion failed.")
        flash("Document deletion failed.", "error")

    return redirect(url_for("documents.document_list"))




