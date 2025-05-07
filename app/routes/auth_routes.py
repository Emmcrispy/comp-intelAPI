from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from app.extensions import db
from app.models.user import User
from app.models.role import Role, user_roles
from app.utils.user_utils import roles_required

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: AdminPass123
    responses:
      201:
        description: User registered successfully
      400:
        description: Bad request or user exists
    """
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify(msg="Missing username or password"), 400
    if User.query.filter_by(username=username).first():
        return jsonify(msg="Username already exists"), 400
    user = User(username=username)
    user.set_password(password)
    # assign default 'user' role
    role = Role.query.filter_by(name='user').first()
    if role:
        user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User registered"), 201

@bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: credentials
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: admin
            password:
              type: string
              example: AdminPass123
    responses:
      200:
        description: Login successful, returns access token
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Missing username or password
      401:
        description: Bad credentials
    """
    # 1) Enforce JSON
    if not request.is_json:
        return jsonify(msg="Request must be JSON"), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(msg="Missing username or password"), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify(msg="Bad credentials"), 401

    # 2) Use a string identity (PyJWT requires sub to be string)
    token = create_access_token(
        identity=user.username,
        additional_claims={"roles": [r.name for r in user.roles]}
    )
    return jsonify(access_token=token), 200

@bp.route('/admin-only', methods=['GET'])
@jwt_required()
@roles_required('admin')
def admin_only():
    """
    Admin-only route
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Welcome, admin!
      403:
        description: Forbidden (non-admin)
      401:
        description: Missing or invalid token
    """
    claims = get_jwt()
    if 'admin' not in claims.get('roles', []):
        return jsonify(msg="Forbidden"), 403
    return jsonify(msg="Welcome, admin!"), 200
