import csv
from io import TextIOWrapper

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.job import Job
from app.services.matching_engine import find_matching_jobs

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')


def parse_csv(stream):
    """
    Simple CSV parser for incoming job uploads.
    Expects a header row matching your Job model's constructor kwargs:
      e.g. title, description, base_rate, sca_code, etc.
    """
    text_io = TextIOWrapper(stream, encoding='utf-8')
    reader = csv.DictReader(text_io)
    for row in reader:
        # Convert numeric fields if present
        if 'base_rate' in row:
            try:
                row['base_rate'] = float(row['base_rate'])
            except (ValueError, TypeError):
                row['base_rate'] = None
        yield row


@bp.route('/search', methods=['GET'])
def search_jobs():
    """
    Search jobs by keyword
    ---
    tags:
      - Jobs
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: keyword(s) to search for
    responses:
      200:
        description: list of matching jobs
        schema:
          type: array
          items:
            $ref: '#/definitions/Job'
    """
    q = request.args.get('q')
    if not q:
        return jsonify(msg="q query parameter required"), 400

    results = Job.query.filter(Job.title.ilike(f'%{q}%')).all()
    return jsonify([r.to_dict() for r in results]), 200


@bp.route('/match', methods=['POST'])
def match_jobs():
    """
    Match a job description against our database
    ---
    tags:
      - Jobs
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: job
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - description
            - keywords
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
        description: matching jobs
        schema:
          type: array
          items:
            $ref: '#/definitions/Job'
    """
    target = request.get_json(force=True)
    matches = find_matching_jobs(target)
    return jsonify([m.to_dict() for m in matches]), 200


@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_jobs():
    """
    Upload job descriptions CSV
    ---
    tags:
      - Jobs
    consumes:
      - multipart/form-data
    produces:
      - application/json
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: CSV file of job descriptions
    responses:
      200:
        description: upload success
        schema:
          type: object
          properties:
            inserted:
              type: integer
    """
    uploaded = request.files.get('file')
    if not uploaded:
        return jsonify(msg="file field required"), 400

    inserted = 0
    for row in parse_csv(uploaded.stream):
        # Map CSV headers into your Job model's fields
        job_data = {
            "function":     row.get("Function"),
            "family":       row.get("Family"),
            "sub_family":   row.get("Sub-Family"),
            "title":        row.get("Title"),
            "career_level": row.get("Career Level"),
            # if you have other fields, map them here, e.g.
            # "base_rate": row.get("Base Rate") or row.get("Salary"),
            # "sca_code":  row.get("SCA Code"),
        }
        # Drop any None values so you don't violate non-null constraints
        filtered = {k: v for k, v in job_data.items() if v is not None}
        job = Job(**filtered)
        db.session.add(job)
        inserted += 1

    db.session.commit()
    return jsonify(inserted=inserted), 200
