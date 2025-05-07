import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret')  # JWT secret, etc.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Default DB URI (to override per environment)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    # Azure Key Vault details (for production)
    KEY_VAULT_NAME = os.getenv('AZURE_KEY_VAULT_NAME')
    BLS_API_KEY = os.getenv('BLS_API_KEY')  # BLS API key (placeholder)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DEV_DATABASE_URI is not set in the environment")

class ProductionConfig(Config):
    DEBUG = False
    # In production, fetch DB URI from Azure Key Vault or environment
    SQLALCHEMY_DATABASE_URI = os.getenv('AZURE_SQL_CONNECTION_STRING', Config.SQLALCHEMY_DATABASE_URI)
