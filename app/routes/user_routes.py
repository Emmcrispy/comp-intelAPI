from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

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
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(
        id=user.id,
        username=user.username,
        roles=[r.name for r in user.roles]
    ), 200
