from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime
from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import get_jwt, get_jwt_identity, create_access_token

from .config     import DevelopmentConfig, ProductionConfig
from .extensions import db, jwt, cors
from app.models.user import User  # so we can load roles into JWTs

# Blueprints
from .routes.main_routes   import bp as main_bp
from .routes.auth_routes   import bp as auth_bp
from .routes.user_routes   import bp as user_bp
from .routes.job_routes    import bp as jobs_bp
from .routes.bls_routes    import bp as bls_bp
from .routes.report_routes import bp as reports_bp

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

    # Debug print to confirm app sees correct URI
    print("→ Using SQLALCHEMY_DATABASE_URI:", app.config['SQLALCHEMY_DATABASE_URI'])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    # Embed roles into every token
    @jwt.additional_claims_loader
    def add_roles(identity):
        user = User.query.filter_by(username=identity).first()
        return {"roles": [r.name for r in user.roles]} if user else {}

    # Sliding‐expiration: refresh token if it's about to expire
    @jwt.token_in_blocklist_loader
    def never_block(jwt_header, jwt_payload):
        return False  # no blacklist by default

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp = get_jwt()["exp"]
            now = datetime.utcnow().timestamp()
            # if fewer than 30 minutes remaining...
            if exp - now < 1800:
                new_token = create_access_token(
                    identity=get_jwt_identity(),
                    fresh=False
                )
                response.headers["X-New-Token"] = new_token
        except Exception:
            pass
        return response

    # Swagger setup
    swagger_conf = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec_1",
                "route":    "/apispec_1.json",
                "rule_filter":  lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    swagger_tpl = {
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
                "description": "JWT: Bearer <token>"
            }
        },
        "security": [
            {"Bearer": []}
        ],
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id":       {"type": "integer"},
                        "username": {"type": "string"},
                        "roles": {
                            "type":  "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }
    }
    Swagger(app, config=swagger_conf, template=swagger_tpl)

    # Register blueprints
    app.register_blueprint(main_bp)    # GET /
    app.register_blueprint(auth_bp)    # /api/auth/*
    app.register_blueprint(user_bp)    # /api/user/*
    app.register_blueprint(jobs_bp)    # /api/jobs/*
    app.register_blueprint(bls_bp)     # /api/bls/*
    app.register_blueprint(reports_bp) # /api/reports/*

    # Register CLI commands (flask init-db, etc.)
    register_commands(app)

    return app
