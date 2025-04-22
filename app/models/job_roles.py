from sqlalchemy import Column, Integer, String
from app.config.db import engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobRole(Base):
    __tablename__ = "job_roles"

    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String, nullable=False)
    job_family = Column(String, nullable=False)
    sub_family = Column(String, nullable=False)
    single_role = Column(String, nullable=False)
    career_level = Column(String, nullable=False)
    country = Column(String, nullable=False)

    title = Column(String)
    skills = Column(String)
    responsibilities = Column(String)

# Optional: create the table if it doesn't exist
Base.metadata.create_all(bind=engine)
