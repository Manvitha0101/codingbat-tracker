from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, index=True) # From CSV
    name = Column(String)
    codingbat_url = Column(String)
    total_solved = Column(Integer, default=0)
    badge = Column(String, default="Beginner")
    
    # Relationship to track history
    history = relationship("ProgressSnapshot", back_populates="student")

class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    solved_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="history")