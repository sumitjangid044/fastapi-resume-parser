from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    skills = Column(String, nullable=True)  # comma-separated
    years_experience = Column(Float, nullable=True)
    target_role = Column(String, nullable=False, index=True)
    eligible = Column(Boolean, default=False)
    resume_filename = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    exam_date = Column(String, nullable=True)
    exam_time = Column(String, nullable=True)
     