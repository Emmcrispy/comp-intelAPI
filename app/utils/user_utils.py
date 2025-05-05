from app.extensions import db
from app.models.user import User
from app.models.role import Role
from werkzeug.security import generate_password_hash, check_password_hash

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
    u = User(username=username)
    u.set_password(password)
    u.roles.append(admin_role)
    db.session.add(u)
    db.session.commit()

def serialize_user(user: User) -> dict:
    """
    Convert a User model instance into a JSON-serializable dict.
    """
    return {
        "id": user.id,
        "username": user.username,
        "roles": [r.name for r in user.roles]
    }
