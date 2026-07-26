from flask import Flask, jsonify
from config import settings
from app.extensions import cors, db, migrate, jwt, swagger
from app.exceptions import register_error_handlers


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
        CORS_ORIGINS=settings.get_cors_origins()
    )

    cors.init_app(app, resources={r"/api/*": {"origins": settings.get_cors_origins()}}, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    register_error_handlers(app)

    from app.api.admin import admin
    from app.api.auth import auth
    from app.api.maintenance import maintenance
    from app.api.manuals import manual
    from app.api.motorcycle import motorcycle
    from app.api.statistic import statistic

    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(motorcycle, url_prefix='/api/motorcycle')
    app.register_blueprint(statistic, url_prefix='/api/statistic')
    app.register_blueprint(maintenance, url_prefix='/api/maintenance')
    app.register_blueprint(manual, url_prefix='/api/manual')
    app.register_blueprint(admin, url_prefix='/api/admin')

    return app