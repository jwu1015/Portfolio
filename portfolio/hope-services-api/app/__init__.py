from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

db = SQLAlchemy()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///hope_services.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    
    # Initialize extensions
    db.init_app(app)
    limiter.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.inventory import inventory_bp
    from app.routes.donations import donations_bp
    from app.routes.orders import orders_bp
    from app.routes.jobs import jobs_bp
    from app.routes.health import health_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(donations_bp, url_prefix='/donations')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    app.register_blueprint(health_bp, url_prefix='/health')
    
    # Initialize Swagger
    from flasgger import Swagger
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Hope Services API",
            "description": "E-commerce and Donations API",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        }
    })
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app


