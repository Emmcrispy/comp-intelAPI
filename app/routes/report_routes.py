import io
import matplotlib.pyplot as plt
import pandas as pd
from flask import Blueprint, request, send_file, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func
from app.extensions import db
from app.models.job import Job
from app.services.matching_engine import find_matching_jobs

bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@bp.route('/salary_distribution', methods=['GET'])
@jwt_required()
def salary_distribution():
    """
    Salary distribution by SCA code
    ---
    tags:
      - Reports
    produces:
      - image/png
    responses:
      200:
        description: PNG bar chart of average base rate per SCA code
    """
    results = db.session.query(Job.sca_code, func.avg(Job.base_rate))\
                        .group_by(Job.sca_code).all()
    codes = [r[0] for r in results]
    avgs  = [r[1] for r in results]

    plt.figure(figsize=(6,4))
    plt.bar(codes, avgs)
    plt.xlabel('SCA Code')
    plt.ylabel('Avg Base Rate')
    plt.title('Avg Base Rate by SCA Code')

    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')


@bp.route('/export/matches', methods=['POST'])
@jwt_required()
def export_matches():
    """
    Export matched jobs as CSV
    ---
    tags:
      - Reports
    consumes:
      - application/json
    produces:
      - text/csv
    parameters:
      - name: body
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
        description: CSV file download
        schema:
          type: string
          format: binary
    """
    target_job = request.get_json(force=True)
    matches    = find_matching_jobs(target_job)
    df = pd.DataFrame([{'id': m.id, 'title': m.title, 'salary': m.base_rate}
                        for m in matches])
    stream = io.BytesIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
    return send_file(stream,
                     as_attachment=True,
                     download_name='matched_jobs.csv',
                     mimetype='text/csv')
