from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProgressSnapshotOut(BaseModel):
    solved_count: int
    timestamp: datetime

    class Config:
        from_attributes = True

class StudentOut(BaseModel):
    student_id: str
    name: str
    total_solved: int
    badge: str

    class Config:
        from_attributes = True

class StudentDetail(StudentOut):
    codingbat_url: str
    history: List[ProgressSnapshotOut] # This sends the data for your graphs!