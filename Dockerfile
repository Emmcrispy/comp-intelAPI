# Use the official slim Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create & use /app as working dir
WORKDIR /app

# Install system dependencies (if any for pyodbc / mssql)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc g++ gnupg2 unixodbc-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Default environment variables (override via docker run or Azure)
ENV FLASK_APP=run.py \
    FLASK_ENV=production

# Use Gunicorn for production‐grade WSGI server
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "run:create_app()"]
