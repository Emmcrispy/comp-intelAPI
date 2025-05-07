from app.extensions import db

class BLSData(db.Model):
    """
    Represents one data point returned from the BLS API.
    Stored in the 'bls_data' table.
    """
    __tablename__ = 'bls_data'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    series_id  = db.Column(db.String(50), nullable=False, index=True)
    year       = db.Column(db.String(4), nullable=False, index=True)
    period     = db.Column(db.String(10), nullable=False)
    value      = db.Column(db.String(20), nullable=False)
    footnotes  = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return (
            f"<BLSData(series_id={self.series_id!r}, "
            f"year={self.year!r}, period={self.period!r}, value={self.value!r})>"
        )
