from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.utils.user_utils import serialize_user

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """
    Get current user's profile
    ---
    tags:
      - User
    security:
      - Bearer: []
    responses:
      200:
        description: Current user details
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                roles:
                  type: array
                  items:
                    type: string
      401:
        description: Missing or invalid token
      404:
        description: User not found
    """
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify(msg="User not found"), 404

    return jsonify(serialize_user(user)), 200
