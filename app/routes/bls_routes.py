import requests
from flask import Blueprint, current_app, request, jsonify
from app.extensions import db
from app.models.bls_data import BLSData

bp = Blueprint('bls', __name__, url_prefix='/api/bls')


@bp.route('/data', methods=['GET'])
def fetch_and_store_bls():
    """
    Fetch BLS timeseries data for a given series ID,
    store each datapoint in Postgres, and return a summary.
    ---
    tags:
      - BLS
    parameters:
      - name: seriesid
        in: query
        type: string
        required: true
        description: BLS series ID (e.g. 'CEU0000000001')
    responses:
      200:
        description: Number of records inserted and full BLS JSON
        schema:
          type: object
          properties:
            inserted:
              type: integer
            data:
              type: object
    """
    series_id = request.args.get('seriesid')
    if not series_id:
        return jsonify(msg="seriesid query parameter required"), 400

    bls_key = current_app.config.get('BLS_API_KEY')
    if not bls_key or bls_key.startswith('<'):
        return jsonify(msg="BLS_API_KEY not configured"), 500

    payload = {"seriesid": [series_id], "registrationKey": bls_key}
    try:
        resp = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                             json=payload, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return jsonify(msg="Failed to fetch from BLS API"), 502

    js = resp.json()
    series = js.get("Results", {}).get("series", [])
    inserted = 0
    for s in series:
        sid = s.get("seriesID")
        for rec in s.get("data", []):
            row = BLSData(
                series_id = sid,
                year      = rec["year"],
                period    = rec["period"],
                value     = rec["value"],
                footnotes = "; ".join(fn.get("text","") for fn in rec.get("footnotes", []))
            )
            db.session.add(row)
            inserted += 1

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify(msg="Database error saving BLS data"), 500

    return jsonify(inserted=inserted, data=js), 200
