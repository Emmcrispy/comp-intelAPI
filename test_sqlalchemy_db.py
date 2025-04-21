import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://erynuser:psppsp12@DESKTOP-KM5FR9B,1433/erynapi?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)

print("🔌 Attempting to connect to:", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Connected successfully to the database!")
        result = conn.execute(text("SELECT GETDATE() AS now"))
        for row in result:
            print("🕒 Current time from SQL Server:", row.now)
except Exception as e:
    print("❌ Connection failed:", e)
