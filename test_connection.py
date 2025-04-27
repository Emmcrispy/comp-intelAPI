#!/usr/bin/env python
"""
test_connection.py

Tests:
  • Database connectivity via DEV_DATABASE_URI
  • BLS.gov API connectivity via BLS_API_KEY
"""

from dotenv import load_dotenv
import os, sys
import requests
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Load .env file
load_dotenv()

def test_db_connection():
    uri = os.getenv('DEV_DATABASE_URI')
    if not uri:
        print("❌ ERROR: DEV_DATABASE_URI environment variable is not set.")
        sys.exit(1)
    print(f"→ Trying database URI: {uri}")
    try:
        engine = create_engine(uri)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful, SELECT 1 returned:", result.scalar())
    except SQLAlchemyError as e:
        print("❌ Database connection failed:")
        print(e)
        sys.exit(1)

def test_bls_api():
    api_key = os.getenv('BLS_API_KEY', '')
    if not api_key or api_key.strip().startswith("<"):
        print("⚠️  BLS_API_KEY is not set or still a placeholder; skipping BLS API test.")
        return
    print(f"→ Testing BLS API with key: {api_key[:4]}...")  # hide most of the key
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {"Content-Type": "application/json"}
    payload = {
        "seriesid": ["CUUR0000SA0"],
        "startyear": "2020",
        "endyear": "2020",
        "registrationkey": api_key
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            print("✅ BLS API connection successful (HTTP 200).")
        else:
            print(f"❌ BLS API returned HTTP {resp.status_code}:")
            print(resp.text)
    except requests.RequestException as e:
        print("❌ BLS API connection failed:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    print("=== Testing Database Connection ===")
    test_db_connection()
    print("\n=== Testing BLS API Connection ===")
    test_bls_api()
    print("\nAll tests completed.")
