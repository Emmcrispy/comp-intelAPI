from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.extensions import db
from app.models.login_history import LoginHistory
from app.models.user          import User
from app.models.role          import Role
from app.utils.user_utils     import authenticate, serialize_user, roles_required

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    consumes:
      - application/json
    produces:
      - application/json
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
              example: user1
            password:
              type: string
              example: Secret123!
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing fields or user already exists
    """
    data = request.get_json(force=True)
    u = data.get('username'); p = data.get('password')
    if not u or not p:
        return jsonify(msg="Missing username or password"), 400
    if User.query.filter_by(username=u).first():
        return jsonify(msg="Username already exists"), 400

    user = User(username=u)
    user.set_password(p)
    role = Role.query.filter_by(name='user').first()
    if role:
        user.roles.append(role)

    db.session.add(user)
    db.session.commit()
    return jsonify(msg="User registered"), 201


@bp.route('/login', methods=['POST'])
def login():
    """
    User login — returns access & refresh tokens and user info
    ---
    tags:
      - Auth
    consumes:
      - application/json
    produces:
      - application/json
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
              example: user1
            password:
              type: string
              example: Secret123!
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user:
              $ref: "#/components/schemas/User"
      400:
        description: Request must be JSON or missing fields
      401:
        description: Bad credentials
    """
    if not request.is_json:
        return jsonify(msg="Request must be JSON"), 400
    data = request.get_json()
    u = data.get('username'); p = data.get('password')
    if not u or not p:
        return jsonify(msg="Missing username or password"), 400

    user = authenticate(u, p)
    if not user:
        return jsonify(msg="Bad credentials"), 401

    # record login history
    evt = LoginHistory(
        user_id    = user.id,
        timestamp  = datetime.utcnow(),
        ip_address = request.remote_addr,
        user_agent = request.headers.get('User-Agent','')
    )
    db.session.add(evt)
    db.session.commit()

    access  = create_access_token(identity=user.username, fresh=True)
    refresh = create_refresh_token(identity=user.username)
    return jsonify(
        access_token  = access,
        refresh_token = refresh,
        user          = serialize_user(user)
    ), 200


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    ---
    tags:
      - Auth
    security:
      - Bearer: []
    produces:
      - application/json
    responses:
      200:
        description: New access token issued
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Missing or invalid refresh token
    """
    identity = get_jwt_identity()
    new_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=new_token), 200


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
    produces:
      - application/json
    responses:
      200:
        description: Welcome, admin!
      403:
        description: Forbidden (non-admin)
      401:
        description: Missing or invalid token
    """
    return jsonify(msg="Welcome, admin!"), 200
