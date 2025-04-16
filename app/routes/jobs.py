from flask import Blueprint, request, jsonify
from app.main import db
from models import Job

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/upload", methods=["POST"])
def upload_job():
    """
    Endpoint for uploading a job description.
    Later, integrate with Azure AI Language for keyword extraction and validation.
    """
    data = request.get_json()
    if not data or not data.get("title") or not data.get("description"):
        return jsonify({"error": "Missing required fields: title and description"}), 400

    # For example, you could add integration with an NLP service here
    # extracted_keywords = azure_ai_extract_keywords(data.get("description"))

    job = Job(
        title=data.get("title"),
        description=data.get("description"),
        skills=data.get("skills")  # This might be enhanced using AI extraction
    )
    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job uploaded successfully",
        "job_id": job.id,
        "job": job.to_dict()
    }), 201

@jobs_bp.route("/search", methods=["GET"])
def search_jobs():
    """
    Endpoint to search for job descriptions.
    Supports filtering by query parameters (e.g., title keyword).
    """
    query = request.args.get("q", None)
    if query:
        jobs = Job.query.filter(Job.title.ilike(f"%{query}%")).all()
    else:
        jobs = Job.query.all()

    results = [job.to_dict() for job in jobs]
    return jsonify(results), 200

@jobs_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    """
    Endpoint for users to submit feedback on matching accuracy,
    which can be used for retraining the matching algorithm.
    """
    data = request.get_json()
    # In a full implementation, save this feedback to a Feedback model/table.
    # Example fields might include: job_id, match_id, relevance_score, notes, etc.
    return jsonify({"message": "Feedback received"}), 200

@jobs_bp.route("/export", methods=["GET"])
def export_results():
    """
    Endpoint to export job search or matching results into CSV/Excel format.
    Currently, this is a placeholder for the export functionality.
    """
    # In a full implementation, query the relevant data and generate a CSV or Excel file.
    return jsonify({"message": "Export feature not implemented yet"}), 200
