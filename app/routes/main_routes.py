from flask import Blueprint, jsonify

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    """
    Home route
    ---
    tags:
      - Main
    responses:
      200:
        description: API is running
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "🚀 Job-Matching API is running"
    """
    return jsonify(message="🚀 Job-Matching API is running"), 200

@bp.route('/api/health', methods=['GET'])
def health():
    """
    Health-check route
    ---
    tags:
      - Main
    responses:
      200:
        description: Service health
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "OK"
    """
    return jsonify(status="OK"), 200
