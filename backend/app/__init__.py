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

    cors.init_app(app, resourses={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'message': 'Hello, yebok!'})

    return app
