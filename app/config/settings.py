import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Comp Intel API"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
