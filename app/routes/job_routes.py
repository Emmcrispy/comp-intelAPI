from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.job import Job
from app.utils.file_utils import process_job_file
from app.services.matching_engine import find_matching_jobs

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_jobs():
    """
    Upload job descriptions
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    requestBody:
      required: true
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              file:
                type: string
                format: binary
    responses:
      200:
        description: Number of jobs uploaded
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
    400:
      description: Invalid file
    security:
      - bearerAuth: []
    """
    file = request.files.get('file')
    if not file:
        return jsonify(msg="No file provided"), 400
    jobs_data = process_job_file(file)
    for row in jobs_data:
        job = Job(**row)
        db.session.add(job)
    db.session.commit()
    return jsonify(msg=f"{len(jobs_data)} jobs uploaded"), 200

@bp.route('/search', methods=['GET'])
@jwt_required()
def search_jobs():
    """
    Search jobs by keyword
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    parameters:
      - name: q
        in: query
        schema:
          type: string
        required: true
        description: Search query
    responses:
      200:
        description: List of matching jobs
        content:
          application/json:
            schema:
              type: object
              properties:
                results:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
                      location:
                        type: string
    400:
      description: Missing query parameter
    security:
      - bearerAuth: []
    """
    q = request.args.get('q')
    if not q:
        return jsonify(msg="Query missing"), 400
    results = Job.query.filter(
        Job.title.ilike(f'%{q}%') | Job.description.ilike(f'%{q}%')
    ).all()
    jobs = [{'id': j.id, 'title': j.title, 'location': j.location} for j in results]
    return jsonify(results=jobs), 200

@bp.route('/match', methods=['POST'])
@jwt_required()
def match_job():
    """
    Match a job description
    ---
    tags:
      - Jobs
    security:
      - Bearer: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              title:
                type: string
              description:
                type: string
              keywords:
                type: array
                items:
                  type: string
    responses:
      200:
        description: List of matched jobs
        content:
          application/json:
            schema:
              type: object
              properties:
                matches:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      title:
                        type: string
    security:
      - bearerAuth: []
    """
    target_job = request.get_json()
    matches = find_matching_jobs(target_job)
    matched = [{'id': m.id, 'title': m.title} for m in matches]
    return jsonify(matches=matched), 200
