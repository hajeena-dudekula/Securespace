import json
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sys

from run import app
from extensions import db
from models.user import User
from models.audit_log import AuditLog
from routes.documents import create_signed_audit_log


TARGET_USERNAME = "hajeenadudekula"


with app.app_context():

    try:
        target = User.query.filter_by(
            username=TARGET_USERNAME
        ).first()

        if not target:
            raise RuntimeError("Target account not found.")

        if target.role != "viewer":
            raise RuntimeError(
                f"Expected viewer role, found: {target.role}"
            )

        admin_count = User.query.filter_by(role="admin").count()

        if admin_count != 0:
            raise RuntimeError(
                "An admin already exists. Bootstrap cancelled."
            )

        old_role = target.role
        target.role = "admin"

        create_signed_audit_log(
            actor_id=None,
            document_id=None,
            action="initial_admin_bootstrapped",
            details=json.dumps({
                "target_user_id": target.id,
                "target_username": target.username,
                "old_role": old_role,
                "new_role": "admin",
                "method": "local_initial_bootstrap"
            }, sort_keys=True),
            ip_address="local-bootstrap"
        )

        db.session.commit()

        print("SUCCESS: Initial admin created.")
        print(f"Username: {target.username}")
        print(f"Role: {target.role}")
        print("Signed audit event recorded.")

    except Exception as error:
        db.session.rollback()
        print(f"BOOTSTRAP FAILED: {error}")
        sys.exit(1)
