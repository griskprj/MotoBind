from flask import Flask, send_from_directory, jsonify
import os
import mimetypes

from app.exceptions import register_error_handlers
from app.extensions import cors, db, jwt, migrate, swagger, mail
from config import settings


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=settings.SECRET_KEY,
        DEBUG=settings.DEBUG,
        SQLALCHEMY_DATABASE_URI=settings.DATABASE_URL,
        SQLALCHEMY_TRACK_MODIFICATIONS=settings.SQLALCHEMY_TRACK_MODIFICATIONS,
        JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
        JWT_ACCESS_TOKEN_EXPIRES=settings.JWT_ACCESS_TOKEN_EXPIRES,
        JWT_REFRESH_TOKEN_EXPIRES=settings.JWT_REFRESH_TOKEN_EXPIRES,
        UPLOAD_FOLDER=settings.UPLOAD_FOLDER,
        MAX_CONTENT_LENGTH=settings.MAX_CONTENT_LENGTH,
        CORS_ORIGINS=settings.get_cors_origins(),
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_USE_SSL=settings.MAIL_USE_SSL,
        MAIL_USE_TLS=settings.MAIL_USE_TLS,
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=settings.MAIL_DEFAULT_SENDER,
    )

    cors.init_app(
        app,
        resources={r"/api/*": {"origins": settings.get_cors_origins()}},
        supports_credentials=True,
    )
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    mail.init_app(app)
    register_error_handlers(app)

    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        """Сервит загруженные файлы"""
        try:
            upload_folder = os.path.abspath(app.config['UPLOAD_FOLDER'])
            file_path = os.path.join(upload_folder, filename)
            
            if not os.path.exists(file_path):
                for root, dirs, files in os.walk(upload_folder):
                    if os.path.basename(filename) in files:
                        rel_path = os.path.relpath(
                            os.path.join(root, os.path.basename(filename)), 
                            upload_folder
                        )
                        return send_from_directory(upload_folder, rel_path)
                
                app.logger.error(f"File not found: {file_path}")
                return jsonify({"error": "File not found"}), 404
            
            return send_from_directory(upload_folder, filename)
            
        except Exception as e:
            app.logger.error(f"Error serving file: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/uploads/<path:filename>')
    def serve_uploaded_file_api(filename):
        """Сервит загруженные файлы через /api"""
        return serve_uploaded_file(filename)

    from app.api.admin import admin
    from app.api.auth import auth
    from app.api.maintenance import maintenance
    from app.api.manuals import manual
    from app.api.motorcycle import motorcycle
    from app.api.statistic import statistic
    from app.api.user import user
    from app.api.notifications import notifications_bp
    from app.api.social import social_bp

    app.register_blueprint(auth, url_prefix="/api/auth")
    app.register_blueprint(motorcycle, url_prefix="/api/motorcycle")
    app.register_blueprint(statistic, url_prefix="/api/statistic")
    app.register_blueprint(maintenance, url_prefix="/api/maintenance")
    app.register_blueprint(manual, url_prefix="/api/manual")
    app.register_blueprint(admin, url_prefix="/api/admin")
    app.register_blueprint(user, url_prefix="/api/user")
    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(social_bp, url_prefix='/api/social')

    return app