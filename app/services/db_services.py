import os
import pyodbc
from dotenv import load_dotenv
from config.settings import settings

redis_host = settings.REDIS_HOST
db_url = settings.DATABASE_URL

load_dotenv()

def get_db_connection():
    try:
        connection_string = (
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')},{os.getenv('DB_PORT')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            f"UID={os.getenv('DB_USER')};"
            f"PWD={os.getenv('DB_PASSWORD')};"
            "Encrypt=no;"  # Local dev: disable encryption unless needed
        )

        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print("❌ DB connection failed:", e)
        raise
