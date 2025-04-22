from sqlalchemy import Column, Integer, String, Text
from app.config.db import Base

class JobUpload(Base):
    __tablename__ = "job_uploads"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    title = Column(String(255))
    skills = Column(Text)
    responsibilities = Column(Text)
    status = Column(String(50), default="pending")  # pending, reviewed, approved
