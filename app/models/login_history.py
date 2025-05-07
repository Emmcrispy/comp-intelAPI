from datetime import datetime
from app.extensions import db

class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)   # supports IPv4 & IPv6
    user_agent = db.Column(db.Text, nullable=True)

    # backref from User
    user = db.relationship("User", back_populates="logins")
