def get_taxonomy_options(stage: str, previous_selection: dict = None):
    """
    Dynamically returns next level of the job taxonomy based on previous selection.
    """

    from sqlalchemy import create_engine, text
    engine = create_engine(DB_URL)
    engine = create_engine(DB_URL)


    query_map = {
        "job_type": "SELECT DISTINCT job_type FROM job_roles ORDER BY job_type;",
        "job_family": "SELECT DISTINCT job_family FROM job_roles WHERE job_type = :job_type ORDER BY job_family;",
        "sub_family": "SELECT DISTINCT sub_family FROM job_roles WHERE job_type = :job_type AND job_family = :job_family ORDER BY sub_family;",
        "single_role": "SELECT DISTINCT single_role FROM job_roles WHERE job_type = :job_type AND job_family = :job_family AND sub_family = :sub_family ORDER BY single_role;",
        "career_level": "SELECT DISTINCT career_level FROM job_roles WHERE job_type = :job_type AND job_family = :job_family AND sub_family = :sub_family AND single_role = :single_role ORDER BY career_level;",
    }

    with engine.connect() as conn:
        query = text(query_map[stage])
        results = conn.execute(query, **previous_selection or  {}).fetchall()
        return [row[0] for row in results]
