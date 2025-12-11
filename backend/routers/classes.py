from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
import database

router = APIRouter(
    prefix="/classes",
    tags=["classes"]
)

get_db = database.get_db

@router.post("/", response_model=schemas.ClassResponse)
def create_class(class_data: schemas.ClassCreate, db: Session = Depends(get_db)):
    # Create new class
    new_class = models.Classes(
        name=class_data.name,
        description=class_data.description,
        teacher_id=class_data.teacher_id
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    
    return new_class

@router.get("/{class_id}", response_model=schemas.ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    # Get class by ID
    class_obj = db.query(models.Classes).filter(models.Classes.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    return class_obj

@router.get("/", response_model=List[schemas.ClassResponse])
def get_classes(teacher_id: int = None, db: Session = Depends(get_db)):
    # Get all classes or classes for a specific teacher
    query = db.query(models.Classes)
    if teacher_id:
        query = query.filter(models.Classes.teacher_id == teacher_id)
    
    return query.all()

@router.post("/{class_id}/enroll", response_model=schemas.ClassEnrollmentResponse)
def enroll_student(class_id: int, enrollment_data: schemas.ClassEnrollmentCreate, db: Session = Depends(get_db)):
    # Check if class exists
    class_obj = db.query(models.Classes).filter(models.Classes.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Check if student is already enrolled
    existing_enrollment = db.query(models.ClassEnrollments).filter(
        models.ClassEnrollments.class_id == class_id,
        models.ClassEnrollments.student_id == enrollment_data.student_id
    ).first()
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Student already enrolled in this class")
    
    # Create new enrollment
    new_enrollment = models.ClassEnrollments(
        class_id=class_id,
        student_id=enrollment_data.student_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return new_enrollment

@router.get("/{class_id}/students", response_model=List[schemas.UserResponse])
def get_class_students(class_id: int, db: Session = Depends(get_db)):
    # Get all students enrolled in a class
    enrollments = db.query(models.ClassEnrollments).filter(
        models.ClassEnrollments.class_id == class_id
    ).all()
    
    student_ids = [enrollment.student_id for enrollment in enrollments]
    students = db.query(models.Users).filter(
        models.Users.id.in_(student_ids),
        models.Users.role == "student"
    ).all()
    
    return students

@router.post("/{class_id}/assign-project", response_model=dict)
def assign_project_to_class(class_id: int, assignment_data: schemas.ClassProjectAssignment, db: Session = Depends(get_db)):
    # Check if class exists
    class_obj = db.query(models.Classes).filter(models.Classes.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Create class-project assignment
    class_project = models.ClassProjects(
        class_id=class_id,
        project_id=assignment_data.project_id
    )
    db.add(class_project)
    db.commit()
    
    return {"message": "Project assigned to class successfully"}

@router.post("/{class_id}/assign-assignment", response_model=dict)
def assign_assignment_to_class(class_id: int, assignment_data: schemas.ClassAssignmentAssignment, db: Session = Depends(get_db)):
    # Check if class exists
    class_obj = db.query(models.Classes).filter(models.Classes.id == class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # Create class-assignment assignment
    class_assignment = models.ClassAssignments(
        class_id=class_id,
        assignment_id=assignment_data.assignment_id
    )
    db.add(class_assignment)
    db.commit()
    
    return {"message": "Assignment assigned to class successfully"}

@router.get("/{class_id}/projects", response_model=List[schemas.ProjectResponse])
def get_class_projects(class_id: int, db: Session = Depends(get_db)):
    # Get all projects assigned to a class
    class_projects = db.query(models.ClassProjects).filter(
        models.ClassProjects.class_id == class_id
    ).all()
    
    project_ids = [cp.project_id for cp in class_projects]
    projects = db.query(models.Projects).filter(
        models.Projects.id.in_(project_ids)
    ).all()
    
    return projects

@router.get("/{class_id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_class_assignments(class_id: int, db: Session = Depends(get_db)):
    # Get all assignments assigned to a class
    class_assignments = db.query(models.ClassAssignments).filter(
        models.ClassAssignments.class_id == class_id
    ).all()
    
    assignment_ids = [ca.assignment_id for ca in class_assignments]
    assignments = db.query(models.Assignments).filter(
        models.Assignments.id.in_(assignment_ids)
    ).all()
    
    return assignments