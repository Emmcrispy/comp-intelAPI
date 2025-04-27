from app.models.job import Job
from app.services.azure_ml import semantic_match

def rule_based_match(job_keywords, jobs, threshold=0.5):
    """Basic rule-based match: match if any keyword in job title/description."""
    matches = []
    for job in jobs:
        text = (job.title + " " + job.description).lower()
        for kw in job_keywords:
            if kw.lower() in text:
                matches.append(job)
                break
    return matches

def find_matching_jobs(target_job):
    """Find matches for a given job description."""
    # Extract keywords via NLP (stub)
    keywords = target_job.get('keywords', [])
    # Get all jobs from DB (in reality, filter by some criteria)
    jobs = Job.query.all()
    # Rule-based matches
    rule_matches = rule_based_match(keywords, jobs)
    # Semantic matches via Azure ML (stub)
    semantic_matches = semantic_match(target_job, jobs)
    # Combine and return unique results
    unique_matches = {job.id: job for job in rule_matches + semantic_matches}
    return list(unique_matches.values())
