
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/", response_model=List[schemas.StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()

@router.get("/{student_id}", response_model=schemas.StudentDetail)
def get_student_progress(student_id: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student