from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
from app.models.user import User

def role_required(required_roles):
    """
    Decorator to protect endpoints by requiring at least one of the given roles.
    Usage:
        @role_required(['admin', 'manager'])
        def some_view(...):
            ...
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_roles = claims.get("roles", [])
            if not any(r in user_roles for r in required_roles):
                return jsonify(msg="Forbidden"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def get_current_user():
    """
    Return the User model instance for the currently
    authenticated JWT identity.
    """
    user_id = get_jwt_identity()
    return User.query.get(user_id)
