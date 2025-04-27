from datetime import datetime
from app.extensions import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # NLP‐extracted attributes
    function = db.Column(db.String(100), nullable=True)
    family = db.Column(db.String(100), nullable=True)
    sub_family = db.Column(db.String(100), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    # SCA & location adjustments
    sca_code = db.Column(db.String(50), nullable=True)
    locality = db.Column(db.String(100), nullable=True)
    # Compensation fields
    base_rate = db.Column(db.Float, nullable=True)
    fringe_benefits = db.Column(db.Float, nullable=True)
    tax_burden = db.Column(db.Float, nullable=True)
    total_cost_per_hour = db.Column(db.Float, nullable=True)
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Job id={self.id} title={self.title!r}>"
