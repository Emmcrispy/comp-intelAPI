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
    security:
      - Bearer: []
    responses:
      200:
        description: PNG bar chart
        content:
          image/png: {}
      401:
        description: Missing or invalid token
    """
    # Aggregate average base_rate by sca_code
    results = (
        db.session.query(Job.sca_code, func.avg(Job.base_rate).label('avg_rate'))
        .group_by(Job.sca_code)
        .all()
    )

    codes = [r.sca_code for r in results]
    avgs  = [float(r.avg_rate) for r in results]

    # Build the chart
    plt.figure()    # one stand-alone figure
    plt.bar(codes, avgs)
    plt.xlabel('SCA Code')
    plt.ylabel('Avg Base Rate')
    plt.title('Avg Base Rate by SCA Code')

    # Return as PNG
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


@bp.route('/export/matches', methods=['POST'])
@jwt_required()
def export_matches():
    """
    Export matched jobs as CSV
    ---
    tags:
      - Reports
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
        description: CSV file download
        content:
          text/csv:
            schema:
              type: string
              format: binary
      400:
        description: Bad request – JSON body required
      401:
        description: Missing or invalid token
    """
    target_job = request.get_json(silent=True)
    if not target_job:
        return jsonify(msg="Bad request: JSON body required"), 400

    # Use your matching engine service
    matches = find_matching_jobs(target_job)

    # Build a DataFrame and stream it out as CSV
    df = pd.DataFrame([
        {'id':    m.id, 'title': m.title, 'salary': m.base_rate}
        for m in matches
    ])
    buf = io.BytesIO()
    df.to_csv(buf, index=False)
    buf.seek(0)

    return send_file(
        buf,
        as_attachment=True,
        download_name='matched_jobs.csv',
        mimetype='text/csv'
    )
