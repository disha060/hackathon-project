from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
import database
from services import adaptive_learning, engagement_tracking, gamification, ai_content_generation

router = APIRouter(
    prefix="/student",
    tags=["student"]
)

get_db = database.get_db

@router.post("/signup", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user (in a real app, hash the password)
    new_user = models.Users(
        name=user.name,
        email=user.email,
        password_hash=user.password,  # In production, hash this!
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # In a real app, verify password hash
    db_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if not db_user or db_user.password_hash != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create fake token for demo
    token_data = schemas.TokenData(email=db_user.email, role=db_user.role)
    return schemas.Token(access_token=f"fake-jwt-token-for-{db_user.email}", token_type="bearer")

@router.get("/mastery", response_model=List[schemas.MasteryResponse])
def get_mastery(db: Session = Depends(get_db)):
    # Return empty list since student hasn't completed any assignments yet
    return []

@router.get("/assignments", response_model=List[schemas.AdaptiveAssignmentResponse])
def get_adaptive_assignments(student_id: int, db: Session = Depends(get_db)):
    # Get adaptive assignments based on student's mastery levels and class enrollment
    # First get classes the student is enrolled in
    enrolled_classes = db.query(models.Classes.id)\
        .join(models.ClassEnrollments)\
        .filter(models.ClassEnrollments.student_id == student_id)\
        .all()
    
    class_ids = [c.id for c in enrolled_classes]
    
    # Get assignments assigned to those classes
    class_assignments = db.query(models.Assignments)\
        .join(models.ClassAssignments)\
        .filter(models.ClassAssignments.class_id.in_(class_ids))\
        .all()
    
    # Convert to adaptive assignment response format
    adaptive_assignments = []
    for assignment in class_assignments:
        adaptive_assignments.append(schemas.AdaptiveAssignmentResponse(
            assignment_id=assignment.id,
            title=assignment.title,
            description=assignment.description,
            difficulty_level=assignment.difficulty_level or 1,
            estimated_time=30  # Default value
        ))
    
    return adaptive_assignments

@router.get("/assignments/{assignment_id}", response_model=schemas.AssignmentResponse)
def get_assignment_by_id(assignment_id: int, db: Session = Depends(get_db)):
    # Get specific assignment by ID
    assignment = db.query(models.Assignments).filter(models.Assignments.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.post("/assignments/submit")
def submit_assignment(student_id: int, assignment_id: int, db: Session = Depends(get_db)):
    # Update student progress, XP, streaks, badges
    gamification.update_after_submission(student_id, assignment_id, db)
    return {"message": "Assignment submitted successfully"}

@router.post("/engagement")
def log_engagement(engagement: schemas.EngagementLogCreate, db: Session = Depends(get_db)):
    # Log engagement and optionally award XP
    engagement_tracking.log_engagement(engagement, db)
    return {"message": "Engagement logged successfully"}

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_projects(student_id: int, db: Session = Depends(get_db)):
    # Get projects that the student is part of through class enrollment
    student_projects = db.query(models.Projects)\
        .join(models.ClassProjects)\
        .join(models.Classes)\
        .join(models.ClassEnrollments)\
        .filter(models.ClassEnrollments.student_id == student_id)\
        .all()
    return student_projects

@router.get("/leaderboard", response_model=List[schemas.LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    # Get class/global leaderboard
    leaderboard = gamification.get_leaderboard(db)
    return leaderboard

@router.get("/badges", response_model=List[schemas.BadgeDisplay])
def get_badges(student_id: int, db: Session = Depends(get_db)):
    # Get student's badges
    badges = gamification.get_student_badges(student_id, db)
    return badges