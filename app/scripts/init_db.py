from app.services.db_services import get_connection

schema_sql = """
CREATE TABLE IF NOT EXISTS job_roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_type VARCHAR(255),
    job_family VARCHAR(255),
    sub_family VARCHAR(255),
    single_role VARCHAR(255),
    career_level VARCHAR(255),
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def create_schema():
    with get_connection() as conn:
        conn.execute(schema_sql)
        print("✅ Schema created successfully.")

if __name__ == "__main__":
    create_schema()
