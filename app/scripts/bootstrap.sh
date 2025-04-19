#!/bin/bash

echo "🚀 Bootstrapping Compensation Intelligence API..."

# Step 1: Activate virtual env
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi
source venv/bin/activate

# Step 2: Install dependencies
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Step 3: Load environment variables
if [ -f ".env" ]; then
    echo "🔐 Loaded local .env variables."
else
    echo "❌ .env file not found!"
fi

# Step 4: Ingest job role data if any
if [ -d "data/uploads" ]; then
    echo "📊 Running automated ingestion..."
    python scripts/auto_ingest.py
fi

# Step 5: Run server
echo "🚀 Starting API server..."
uvicorn app.main:app --reload
