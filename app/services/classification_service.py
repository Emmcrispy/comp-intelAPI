from sqlalchemy import create_engine, text
from app.services.cache_service import cache_get, cache_set
from app.config.settings import settings

def get_taxonomy_options(stage: str, previous_selection: dict = None):
    engine = create_engine(settings.DATABASE_URL)

    # SQL query map per dropdown level
    query_map = {
        "job_type": "SELECT DISTINCT job_type FROM job_roles ORDER BY job_type;",
        "job_family": """
            SELECT DISTINCT job_family FROM job_roles
            WHERE job_type = :job_type
            ORDER BY job_family;
        """,
        "sub_family": """
            SELECT DISTINCT sub_family FROM job_roles
            WHERE job_type = :job_type AND job_family = :job_family
            ORDER BY sub_family;
        """,
        "single_role": """
            SELECT DISTINCT single_role FROM job_roles
            WHERE job_type = :job_type AND job_family = :job_family AND sub_family = :sub_family
            ORDER BY single_role;
        """,
        "career_level": """
            SELECT DISTINCT career_level FROM job_roles
            WHERE job_type = :job_type AND job_family = :job_family AND sub_family = :sub_family AND single_role = :single_role
            ORDER BY career_level;
        """
    }

    with engine.connect() as conn:
        query = text(query_map[stage])
        results = conn.execute(query, previous_selection or {}).fetchall()
        return [row[0] for row in results]
