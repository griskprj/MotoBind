from flask import Flask, jsonify
from config import Config
from app.extensions import cors, db, migrate, jwt


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
    
    with app.app_context():
        from app.models.user import User
        from app.models.maintenance import Maintenance
        from app.models.motorcycles import Motorcycle

    from app.api.auth import auth
    
    app.register_blueprint(auth, url_prefix='/api/auth')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'message': 'Hello, yebok!'})

    return app
