from flask import Blueprint, request, jsonify, current_app

bp = Blueprint('bls', __name__, url_prefix='/api/bls')

@bp.route('/data', methods=['GET'])
def get_bls_data():
    """
    Fetch BLS.gov data
    ---
    tags:
      - BLS
    parameters:
      - name: seriesid
        in: query
        schema:
          type: array
          items:
            type: string
        required: true
        explode: true
      - name: startyear
        in: query
        schema:
          type: string
        required: true
      - name: endyear
        in: query
        schema:
          type: string
        required: true
    responses:
      200:
        description: Raw BLS API response
        content:
          application/json:
            schema:
              type: object
    400:
      description: Missing parameters
    """
    series = request.args.getlist('seriesid')
    start = request.args.get('startyear')
    end = request.args.get('endyear')
    if not series or not start or not end:
        return jsonify(msg="Missing parameters"), 400
    import requests
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    headers = {'Content-type': 'application/json'}
    payload = {
        "seriesid": series,
        "startyear": start,
        "endyear": end,
        "registrationkey": current_app.config.get('BLS_API_KEY')
    }
    resp = requests.post(url, json=payload, headers=headers)
    return jsonify(resp.json())
