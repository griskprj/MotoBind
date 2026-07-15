from flask import Flask, jsonify
from config import Config
from app.extensions import cors, db, migrate, jwt, swagger
from app.exceptions import register_error_handlers



def create_app(config_class=Config):
    """ App fabric 
    
    Init extensions:
        > cors - CORS
        > db - Database
        > migrate - Database migrations
        > jwt - Jwt manager
    
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    cors.init_app(app, resourses={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    register_error_handlers(app)
    
    with app.app_context():
        from app.models.user import User
        from app.models.maintenance import Maintenance
        from app.models.motorcycle import Motorcycle

    from app.api.auth import auth
    from app.api.motorcycle import motorcycle
    from app.api.statistic import statistic
    from app.api.maintenance import maintenance
    from app.api.manuals import manual
    from app.api.admin import admin

    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(motorcycle, url_prefix='/api/motorcycle')
    app.register_blueprint(statistic, url_prefix='/api/statistic')
    app.register_blueprint(maintenance, url_prefix='/api/maintenance')
    app.register_blueprint(manual, url_prefix='/api/manual')
    app.register_blueprint(admin, url_prefix='/api/admin')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'message': 'Hello, yebok!'})

    return app
