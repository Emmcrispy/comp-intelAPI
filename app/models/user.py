from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.role import Role, user_roles

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    # many-to-many with roles
    roles = db.relationship('Role', secondary=user_roles, backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User id={self.id} username={self.username!r}>"
