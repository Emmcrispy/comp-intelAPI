# app/routes/bls_routes.py

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

    Query Parameters:
        - seriesid (required): The BLS series ID to fetch (e.g. 'CEU0000000001').

    Responses:
        200: { inserted: <int>, data: <full BLS JSON> }
        400: Missing or invalid parameters
        500: Upstream or database error
    """
    series_id = request.args.get('seriesid')
    if not series_id:
        return jsonify(msg="seriesid query parameter required"), 400

    # 1) Call the BLS API
    bls_key = current_app.config.get('BLS_API_KEY')
    if not bls_key or bls_key.startswith('<'):
        return jsonify(msg="BLS_API_KEY not configured"), 500

    payload = {
        "seriesid": [series_id],
        "registrationKey": bls_key
    }

    try:
        bls_resp = requests.post(
            "https://api.bls.gov/publicAPI/v2/timeseries/data/",
            json=payload,
            timeout=10
        )
        bls_resp.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error("BLS API request failed: %s", e)
        return jsonify(msg="Failed to fetch from BLS API"), 502

    js = bls_resp.json()
    results = js.get("Results", {}).get("series", [])
    if not results:
        return jsonify(msg="No data returned from BLS"), 404

    # 2) Persist into Postgres
    inserted = 0
    for series in results:
        sid = series.get("seriesID")
        for rec in series.get("data", []):
            # Optional: skip duplicates if you have a uniqueness constraint
            row = BLSData(
                series_id = sid,
                year      = rec.get("year"),
                period    = rec.get("period"),
                value     = rec.get("value"),
                footnotes = "; ".join(fn.get("text","") for fn in rec.get("footnotes", []))
            )
            db.session.add(row)
            inserted += 1

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error("DB commit failed: %s", e)
        db.session.rollback()
        return jsonify(msg="Database error saving BLS data"), 500

    return jsonify(inserted=inserted, data=js), 200
