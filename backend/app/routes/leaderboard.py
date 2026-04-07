from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.badge_service import calculate_badges

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    # The '.desc()' ensures the Gold winner is first in the list
    students = db.query(models.Student).order_by(models.Student.total_solved.desc()).all()
    
    # This applies 'Top Performer', etc.
    ranked_students = calculate_badges(students)
    return ranked_students