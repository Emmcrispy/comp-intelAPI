import os
from flask import Flask
from flasgger import Swagger
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, jwt, cors, swagger
from .routes import auth_routes, job_routes, bls_routes, report_routes
from .routes.main_routes import bp as main_bp
from .routes.user_routes import bp as user_bp
from .commands import init_app as register_commands


def create_app():
    app = Flask(__name__)
    # Choose config based on environment
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
        # Optionally override from Key Vault:
        # app.config['SQLALCHEMY_DATABASE_URI'] = get_secret('AzureSQLConnectionString')
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Swagger configuration
    app.config['SWAGGER'] = {
        "title": "Compensation API",
        "openapi": "3.0.2",
        "uiversion": 3,
        "specs": [  # include all routes
            {
                "endpoint": "apispec_1",
                "route": "/apispec_1.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "specs_route": "/apidocs/",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        },
        "security": [
            { "Bearer": [] }
        ]
    }
    swagger.init_app(app)

    # Register main & health-check routes
    app.register_blueprint(main_bp)

    # Register blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(job_routes.bp)
    app.register_blueprint(bls_routes.bp)
    app.register_blueprint(report_routes.bp)
    app.register_blueprint(user_bp)

    register_commands(app)

    return app
