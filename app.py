from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from flask_wtf.csrf import CSRFProtect

from extensions import db, limiter

csrf = CSRFProtect()
from config import Config
from models.user import User
from models.document import Document
from models.permission import DocumentPermission
from models.audit_log import AuditLog
from routes.auth import auth
from routes.documents import documents


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object(Config)
    app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth)
    app.register_blueprint(documents)

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.route("/dashboard")
    @login_required
    def dashboard():
        return render_template(
            "dashboard.html",
            username=current_user.username,
            role=current_user.role
        )

    @app.route("/admin/activity")
    @login_required
    def admin_activity():

        if current_user.role != "admin":
            return "Access denied", 403

        activities = AuditLog.query.order_by(
            AuditLog.created_at.desc()
        ).limit(100).all()

        return render_template(
            "admin/activity.html",
            activities=activities
        )
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)




from models.permission import DocumentPermission
from models.audit_log import AuditLog
