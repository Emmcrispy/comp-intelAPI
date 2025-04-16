from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database connection
    db.init_app(app)

    # Import and register blueprints
    from routes.jobs import jobs_bp
    from app.dependencies.auth import auth_bp  # Stub for authentication endpoints
    app.register_blueprint(jobs_bp, url_prefix="/api/v1/jobs")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    @app.route('/')
    def home():
        return "erynAI Compensation Intelligence API!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
