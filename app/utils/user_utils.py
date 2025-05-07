from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.user import User
from app.models.role import Role


def create_default_roles():
    """
    Ensure the standard roles exist in the database.
    """
    for name in ("admin", "user"):
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
    db.session.commit()


def seed_admin_user(username: str, password: str):
    """
    Create an initial admin user if it doesn't already exist.
    """
    if User.query.filter_by(username=username).first():
        return

    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        raise RuntimeError("Run create_default_roles() first.")

    # Hash the password here instead of relying on a model helper
    pw_hash = generate_password_hash(password)
    u = User(username=username, password_hash=pw_hash)
    u.roles.append(admin_role)

    db.session.add(u)
    db.session.commit()


def authenticate(username: str, password: str) -> User | None:
    """
    Verify username & password. Return the User if valid, else None.
    """
    user = User.query.filter_by(username=username).first()
    if not user or not user.password_hash:
        return None
    if check_password_hash(user.password_hash, password):
        return user
    return None


def serialize_user(user: User) -> dict:
    """
    Convert a User model instance into a JSON-serializable dict.
    """
    return {
        "id": user.id,
        "username": user.username,
        "roles": [r.name for r in user.roles]
    }


def roles_required(*required_roles):
    """
    Decorator to protect a route so that only JWTs carrying at least one
    of the `required_roles` in their 'roles' claim can pass.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1) Ensure there's a valid JWT in the request
            verify_jwt_in_request()

            # 2) Read the 'roles' claim from the token
            claims = get_jwt()
            user_roles = claims.get("roles", [])

            # 3) If none of the required roles are present, forbid access
            if not any(role in user_roles for role in required_roles):
                return jsonify(msg="Forbidden: insufficient privileges"), 403

            # 4) Otherwise, call the view
            return fn(*args, **kwargs)
        return decorator
    return wrapper
