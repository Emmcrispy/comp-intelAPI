from sqlalchemy import Column, Integer, String, Text
from app.config.db import Base

class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String(255))
    job_family = Column(String(255))
    sub_family = Column(String(255))
    single_role = Column(String(255))
    career_level = Column(String(255))
    country = Column(String(255))
    description = Column(Text)
    title = Column(String(255))
    skills = Column(Text)
    responsibilities = Column(Text)
