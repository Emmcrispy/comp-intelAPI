import os

class Config:
    # For deployment, replace with  Azure SQL Database URL or other connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///compensation.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "change_this_to_a_secure_value"
