from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flasgger import Swagger

from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, jwt, cors

# We need the User model to load roles into JWTs
from app.models.user import User

# Import each Blueprint
from .routes.auth_routes   import bp as auth_bp
from .routes.job_routes    import bp as jobs_bp
from .routes.bls_routes    import bp as bls_bp
from .routes.report_routes import bp as reports_bp
from .routes.main_routes   import bp as main_bp
from .routes.user_routes   import bp as user_bp

from .commands import init_app as register_commands


def create_app():
    app = Flask(__name__)

    # Load config
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Debug print to confirm the DB URI is loaded correctly
    print("→ Using SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Embed roles into every access token
    @jwt.additional_claims_loader
    def add_roles_to_claims(identity):
        """
        Adds a 'roles' claim to the JWT from the user's roles in the database.
        `identity` here is the username we passed to create_access_token().
        """
        user = User.query.filter_by(username=identity).first()
        return {"roles": [r.name for r in user.roles]} if user else {}

    # --- Swagger / OpenAPI Setup ---
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route":    "/apispec_1.json",
                "rule_filter":  lambda rule: True,   # include all routes
                "model_filter": lambda tag: True     # include all models
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title":       "Compensation API",
            "version":     "1.0.0",
            "description": "Production-ready Flask API for compensation analytics, Azure AI & ML enabled"
        },
        "securityDefinitions": {
            "Bearer": {
                "type":        "apiKey",
                "name":        "Authorization",
                "in":          "header",
                "description": (
                    "JWT authorization header using the Bearer scheme. "
                    "Enter: **Bearer <your JWT>**"
                )
            }
        },
        # Apply the Bearer security scheme globally to all endpoints
        "security": [
            { "Bearer": [] }
        ]
    }

    # Instantiate Swagger with both config & template so the Authorize UI appears
    Swagger(app, config=swagger_config, template=swagger_template)

    # Register blueprints
    app.register_blueprint(main_bp)                          # GET /
    app.register_blueprint(auth_bp,    url_prefix='/api/auth')
    app.register_blueprint(jobs_bp,    url_prefix='/api/jobs')
    app.register_blueprint(bls_bp,     url_prefix='/api/bls')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(user_bp,    url_prefix='/api/user')

    # Register CLI commands (e.g. flask init-db)
    register_commands(app)

    return app
