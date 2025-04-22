import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Comp Intel API"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    DATABASE_URL = os.getenv("DATABASE_URL")

    def __init__(self):
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL not set. Check your .env configuration.")

settings = Settings()
