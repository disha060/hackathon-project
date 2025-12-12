from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import schemas
import models
import database
from services import adaptive_learning, engagement_tracking, gamification, ai_content_generation
from sqlalchemy import and_
from auth_utils import get_current_student, get_current_user

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
def get_mastery(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get student mastery records
    student_id = current_user.id
    mastery_records = db.query(models.StudentMastery).filter(
        models.StudentMastery.student_id == student_id
    ).all()
    
    results = []
    for record in mastery_records:
        results.append({
            "concept_id": record.concept_id,
            "concept_name": record.concept.name if record.concept else "Unknown",
            "mastery_score": record.mastery_score,
            "level": int(record.mastery_score / 20) + 1
        })
    return results

@router.get("/assignments/adaptive", response_model=List[schemas.AdaptiveAssignmentResponse])
def get_adaptive_assignments(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get adaptive assignments based on student's mastery levels and class enrollment
    student_id = current_user.id
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

@router.get("/assignments/{assignment_id}/info", response_model=schemas.AssignmentResponse)
def get_assignment_by_id(
    assignment_id: int, 
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_user)
):
    # Get specific assignment by ID
    assignment = db.query(models.Assignments).filter(models.Assignments.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.post("/engagement")
def log_engagement(engagement: schemas.EngagementLogCreate, db: Session = Depends(get_db)):
    # Log engagement and optionally award XP
    engagement_tracking.log_engagement(engagement, db)
    return {"message": "Engagement logged successfully"}

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_projects(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get projects that the student is part of through class enrollment
    student_id = current_user.id
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
def get_badges(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get student's badges and achievements
    student_id = current_user.id
    badges = gamification.get_student_badges(student_id, db)
    return badges

@router.get("/assignments", response_model=List[schemas.StudentAssignmentDetail])
async def get_student_assignments(
    status: Optional[schemas.AssignmentStatus] = None,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get all assignments for the student with their status
    student_id = current_user.id
    query = db.query(models.StudentAssignments).filter(models.StudentAssignments.student_id == student_id)
    
    if status:
        query = query.filter(models.StudentAssignments.status == status)
    
    student_assignments = query.all()
    
    result = []
    for sa in student_assignments:
        assignment = db.query(models.Assignments).filter(models.Assignments.id == sa.assignment_id).first()
        if not assignment: continue
        
        # Find due date based on the class the student is enrolled in
        due_date = None
        student_classes = db.query(models.ClassEnrollments.class_id).filter(
            models.ClassEnrollments.student_id == student_id
        ).all()
        student_class_ids = [c.class_id for c in student_classes]
        
        if student_class_ids:
            class_assignment = db.query(models.ClassAssignments).filter(
                models.ClassAssignments.assignment_id == sa.assignment_id,
                models.ClassAssignments.class_id.in_(student_class_ids)
            ).first()
            if class_assignment:
                due_date = class_assignment.due_date
        
        # Add to result list
        result.append({
            **assignment.__dict__,
            "status": sa.status,
            "score": sa.score,
            "submitted_at": sa.submitted_at,
            "due_date": due_date
        })
    
    return result

@router.get("/assignments/{assignment_id}", response_model=schemas.StudentAssignmentDetail)
async def get_assignment_details(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get assignment details with student's submission status
    student_id = current_user.id
    assignment = db.query(
        models.Assignments,
        models.StudentAssignments.status,
        models.StudentAssignments.score,
        models.StudentAssignments.submitted_at,
        models.ClassAssignments.due_date
    ).join(
        models.StudentAssignments,
        and_(
            models.Assignments.id == models.StudentAssignments.assignment_id,
            models.StudentAssignments.student_id == student_id
        )
    ).outerjoin(
        models.ClassAssignments,
        models.Assignments.id == models.ClassAssignments.assignment_id
    ).filter(
        models.Assignments.id == assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found or not assigned to student"
        )
    
    return {
        **assignment[0].__dict__,
        "status": assignment[1],
        "score": assignment[2],
        "submitted_at": assignment[3],
        "due_date": assignment[4]
    }

@router.post("/assignments/{assignment_id}/submit", status_code=status.HTTP_200_OK)
async def submit_assignment(
    assignment_id: int,
    submission: schemas.AssignmentSubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Check if assignment exists and is assigned to student
    student_id = current_user.id
    
    student_assignment = db.query(models.StudentAssignments).filter(
        models.StudentAssignments.assignment_id == assignment_id,
        models.StudentAssignments.student_id == student_id
    ).first()
    
    if not student_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found or not assigned to student"
        )
    
    # Update submission details
    student_assignment.status = schemas.AssignmentStatus.SUBMITTED
    student_assignment.submission_url = submission.submission_url
    student_assignment.submission_notes = submission.submission_notes
    student_assignment.submitted_at = datetime.utcnow()
    
    # Log engagement
    engagement_log = models.EngagementLogs(
        student_id=student_id,
        engagement_type=schemas.EngagementType.ASSIGNMENT,
        value=1,  # Count as one engagement
        metadata_json=f"{{'assignment_id': {assignment_id}, 'action': 'submission'}}"
    )
    
    db.add(engagement_log)
    db.commit()
    db.refresh(student_assignment)
    
    # Update student progress, XP, streaks, badges
    gamification.update_after_submission(student_id, assignment_id, db)
    
    # TODO: Send notification to teacher
    
    return {"message": "Assignment submitted successfully", "assignment_id": assignment_id}

@router.get("/assignments/{assignment_id}/status", response_model=schemas.StudentAssignmentDetail)
async def get_assignment_status(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_student)
):
    # Get assignment status for student
    student_id = current_user.id
    assignment = db.query(
        models.Assignments,
        models.StudentAssignments.status,
        models.StudentAssignments.score,
        models.StudentAssignments.submitted_at,
        models.ClassAssignments.due_date
    ).join(
        models.StudentAssignments,
        and_(
            models.Assignments.id == models.StudentAssignments.assignment_id,
            models.StudentAssignments.student_id == student_id
        )
    ).outerjoin(
        models.ClassAssignments,
        models.Assignments.id == models.ClassAssignments.assignment_id
    ).filter(
        models.Assignments.id == assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found or not assigned to student"
        )
    
    return {
        **assignment[0].__dict__,
        "status": assignment[1],
        "score": assignment[2],
        "submitted_at": assignment[3],
        "due_date": assignment[4]
    }