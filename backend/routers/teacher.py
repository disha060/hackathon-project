from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import schemas
import models
import database
from services import ai_content_generation, teacher_interventions
import asyncio
from auth_utils import get_current_teacher

router = APIRouter(
    prefix="/teacher",
    tags=["teacher"]
)

get_db = database.get_db

@router.get("/ai/assignments", response_model=List[schemas.AIGeneratedAssignment])
def get_ai_assignments(concept_id: int, api_key: Optional[str] = None, db: Session = Depends(get_db)):
    # Get AI-suggested assignments for a concept
    assignments = ai_content_generation.generate_assignments(concept_id, db, api_key)
    return assignments

@router.post("/assignments/create")
def create_assignment(
    assignments: List[schemas.AssignmentCreate], 
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_teacher)
):
    # Teacher selects AI-generated assignment(s) to assign
    created_assignments = []
    for assignment in assignments:
        db_assignment = models.Assignments(**assignment.dict(), teacher_id=current_user.id)
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        created_assignments.append(db_assignment)
    
    return {"message": f"Created {len(created_assignments)} assignments", "assignments": created_assignments}

@router.post("/assignments", response_model=schemas.AssignmentResponse)
def create_and_assign_assignment(
    assignment_data: schemas.AssignmentCreateWithClasses,
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_teacher)
):
    # Create assignment
    db_assignment = models.Assignments(
        title=assignment_data.title,
        description=assignment_data.description,
        concept_id=assignment_data.concept_id,
        difficulty_level=assignment_data.difficulty_level,
        content_url=assignment_data.content_url,
        teacher_id=current_user.id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    
    # Assign to classes and students
    for class_id in assignment_data.class_ids:
        # Create class assignment
        class_assignment = models.ClassAssignments(
            class_id=class_id,
            assignment_id=db_assignment.id,
            due_date=assignment_data.due_date
        )
        db.add(class_assignment)
        
        # Get students in class
        enrollments = db.query(models.ClassEnrollments).filter(
            models.ClassEnrollments.class_id == class_id
        ).all()
        
        # Assign to students
        for enrollment in enrollments:
            # Check if already assigned
            existing = db.query(models.StudentAssignments).filter(
                models.StudentAssignments.student_id == enrollment.student_id,
                models.StudentAssignments.assignment_id == db_assignment.id
            ).first()
            
            if not existing:
                student_assignment = models.StudentAssignments(
                    student_id=enrollment.student_id,
                    assignment_id=db_assignment.id,
                    status=schemas.AssignmentStatus.ASSIGNED
                )
                db.add(student_assignment)
                
    db.commit()
    return db_assignment

@router.get("/assignments", response_model=List[schemas.AssignmentWithClassesResponse])
def get_teacher_assignments(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_teacher)
):
    """Get all assignments created by the current teacher with class details"""
    assignments = db.query(models.Assignments).filter(models.Assignments.teacher_id == current_user.id).all()
    
    result = []
    for assignment in assignments:
        # Get classes for this assignment
        class_assignments = db.query(models.ClassAssignments).filter(
            models.ClassAssignments.assignment_id == assignment.id
        ).all()
        
        classes = []
        for ca in class_assignments:
            cls = db.query(models.Classes).filter(models.Classes.id == ca.class_id).first()
            if cls:
                classes.append(schemas.ClassSimple(id=cls.id, name=cls.name))
        
        # Convert to response model
        assignment_dict = assignment.__dict__
        assignment_dict["classes"] = classes
        result.append(assignment_dict)
        
    return result

@router.get("/ai/projects", response_model=List[schemas.AIGeneratedProject])
def get_ai_projects(skill_area: str, api_key: Optional[str] = None, db: Session = Depends(get_db)):
    # Get AI-suggested projects for a skill area
    projects = ai_content_generation.generate_projects(skill_area, db, api_key)
    return projects

@router.post("/projects/create")
def create_project(projects: List[schemas.ProjectCreate], db: Session = Depends(get_db)):
    # Teacher approves AI-generated project and assigns to students
    created_projects = []
    for project in projects:
        db_project = models.Projects(**project.dict())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        created_projects.append(db_project)
    
    return {"message": f"Created {len(created_projects)} projects", "projects": created_projects}

@router.post("/softskills/score")
def score_soft_skills(scores: List[schemas.SoftSkillScoreCreate], db: Session = Depends(get_db)):
    # Record peer/teacher ratings for soft skills
    created_scores = []
    for score in scores:
        db_score = models.SoftSkillScores(**score.dict())
        db.add(db_score)
        db.commit()
        db.refresh(db_score)
        created_scores.append(db_score)
    
    return {"message": f"Recorded {len(created_scores)} soft skill scores", "scores": created_scores}

@router.get("/classes", response_model=List[schemas.ClassResponse])
async def get_teacher_classes(
    current_user: models.Users = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    """
    Get all classes for the current teacher
    """
    classes = db.query(models.Classes).filter(
        models.Classes.teacher_id == current_user.id
    ).all()
    return classes

@router.get("/students", response_model=List[schemas.UserResponse])
def get_all_students(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_teacher)
):
    """Get all students in the system"""
    students = db.query(models.Users).filter(models.Users.role == "student").all()
    return students

@router.get("/teachers", response_model=List[schemas.UserResponse])
def get_all_teachers(
    db: Session = Depends(get_db),
    current_user: models.Users = Depends(get_current_teacher)
):
    """Get all teachers in the system"""
    teachers = db.query(models.Users).filter(models.Users.role == "teacher").all()
    return teachers

@router.get("/dashboard")
def get_dashboard(teacher_id: int, db: Session = Depends(get_db)):
    # Get class-wide mastery, engagement, soft skills, leaderboard
    dashboard_data = teacher_interventions.get_class_dashboard(teacher_id, db)
    return dashboard_data

@router.post("/intervene")
def intervene(intervention: schemas.TeacherInterventionCreate, db: Session = Depends(get_db)):
    # Intervene with struggling students
    db_intervention = models.TeacherInterventions(**intervention.dict())
    db.add(db_intervention)
    db.commit()
    db.refresh(db_intervention)
    
    return {"message": "Intervention recorded", "intervention": db_intervention}

@router.post("/ai/generate-quiz", response_model=schemas.GeneratedQuiz)
async def generate_quiz(topic: str, difficulty: int = 3, question_count: int = 5, api_key: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Generate quiz questions using the Gemini API.
    
    Args:
        topic: The topic for the quiz
        difficulty: Difficulty level (1-5)
        question_count: Number of questions to generate (1-10)
        api_key: Optional Gemini API key. If not provided, will use from environment.
        
    Returns:
        GeneratedQuiz: A quiz with questions and answers
    """
    # Validate inputs
    difficulty = max(1, min(5, difficulty))  # Clamp difficulty between 1-5
    question_count = max(1, min(10, question_count))  # Clamp between 1-10 questions
    
    # Map numeric difficulty to string for the API
    difficulty_map = {
        1: "beginner",
        2: "easy",
        3: "medium",
        4: "hard",
        5: "expert"
    }
    difficulty_str = difficulty_map.get(difficulty, "medium")
    
    try:
        # Generate quiz questions using our new function
        questions_data = await ai_content_generation.generate_quiz_questions(
            topic=topic,
            num_questions=question_count,
            difficulty=difficulty_str,
            api_key=api_key
        )
        
        # Convert to QuizQuestion objects
        questions = []
        for i, q in enumerate(questions_data):
            questions.append(schemas.QuizQuestion(
                id=i+1,
                type=q.get("type", "Multiple Choice"),
                question=q.get("question", ""),
                options=q.get("options", None),
                correct_answer=str(q.get("correct_answer", "")),
                explanation=q.get("explanation", "")
            ))
        
        return schemas.GeneratedQuiz(
            topic=topic,
            difficulty=difficulty,
            questions=questions
        )
        
    except Exception as e:
        # Fallback to template-based generation if API call fails
        print(f"Error generating quiz: {str(e)}")
        questions = []
        question_types = ['Multiple Choice', 'True or False', 'Short Answer', 'Fill in the Blank']
        
        for i in range(question_count):
            question_type = question_types[i % len(question_types)]
            
            if question_type == 'Multiple Choice':
                questions.append(schemas.QuizQuestion(
                    id=i+1,
                    type=question_type,
                    question=f"What is a key aspect of {topic}?",
                    options=[f"Aspect {i+1}A", f"Aspect {i+1}B", f"Aspect {i+1}C", f"Aspect {i+1}D"],
                    correct_answer=f"Aspect {i+1}B",
                    explanation="This is a sample explanation. The correct answer is Aspect B."
                ))
            elif question_type == 'True or False':
                questions.append(schemas.QuizQuestion(
                    id=i+1,
                    type=question_type,
                    question=f"{topic} is an important subject.",
                    options=None,
                    correct_answer="True",
                    explanation=f"{topic} is indeed an important subject as it covers fundamental concepts."
                ))
            else:
                questions.append(schemas.QuizQuestion(
                    id=i+1,
                    type=question_type,
                    question=f"Explain a key concept of {topic}.",
                    options=None,
                    correct_answer=f"Key concept explanation for {topic}",
                    explanation=f"A key concept in {topic} is that it provides a foundation for understanding more advanced topics."
                ))
        
        return schemas.GeneratedQuiz(
            topic=topic,
            difficulty=difficulty,
            questions=questions
        )

@router.get("/interventions", response_model=List[schemas.TeacherInterventionResponse])
async def get_interventions(teacher_id: int, db: Session = Depends(get_db)):
    interventions = teacher_interventions.get_interventions(teacher_id, db)
    return interventions

@router.post("/assignments/class/{class_id}", status_code=status.HTTP_201_CREATED)
async def assign_to_class(
    class_id: int, 
    assignment_data: schemas.ClassAssignmentAssignment,
    db: Session = Depends(get_db)
):
    # Check if class exists
    db_class = db.query(models.Classes).filter(models.Classes.id == class_id).first()
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found"
        )
    
    # Check if assignment exists
    assignment = db.query(models.Assignments).filter(
        models.Assignments.id == assignment_data.assignment_id
    ).first()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assignment with id {assignment_data.assignment_id} not found"
        )
    
    # Create class assignment
    db_class_assignment = models.ClassAssignments(
        class_id=class_id,
        assignment_id=assignment_data.assignment_id,
        assigned_at=datetime.utcnow()
    )
    
    # Get all students in the class
    class_enrollments = db.query(models.ClassEnrollments).filter(
        models.ClassEnrollments.class_id == class_id
    ).all()
    
    # Assign to each student
    for enrollment in class_enrollments:
        student_assignment = models.StudentAssignments(
            student_id=enrollment.student_id,
            assignment_id=assignment_data.assignment_id,
            status=schemas.AssignmentStatus.ASSIGNED
        )
        db.add(student_assignment)
    
    db.add(db_class_assignment)
    db.commit()
    db.refresh(db_class_assignment)
    
    return {"message": f"Assignment {assignment.title} assigned to class {db_class.name}"}

@router.get("/classes/{class_id}/assignments", response_model=List[schemas.ClassAssignmentResponse])
async def get_class_assignments(class_id: int, db: Session = Depends(get_db)):
    # Get all assignments for the class with their details
    assignments = db.query(
        models.Assignments,
        models.ClassAssignments.assigned_at,
        models.ClassAssignments.due_date
    ).join(
        models.ClassAssignments,
        models.Assignments.id == models.ClassAssignments.assignment_id
    ).filter(
        models.ClassAssignments.class_id == class_id
    ).all()
    
    return [
        {
            **assignment[0].__dict__,
            "assigned_at": assignment[1],
            "due_date": assignment[2],
            "class_id": class_id
        }
        for assignment in assignments
    ]

@router.get("/assignments/{assignment_id}/submissions", response_model=List[schemas.AssignmentSubmissionResponse])
async def get_assignment_submissions(
    assignment_id: int,
    class_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.StudentAssignments).filter(
        models.StudentAssignments.assignment_id == assignment_id
    )
    
    if class_id:
        # Get only submissions from students in the specified class
        query = query.join(
            models.ClassEnrollments,
            models.StudentAssignments.student_id == models.ClassEnrollments.student_id
        ).filter(
            models.ClassEnrollments.class_id == class_id
        )
    
    submissions = query.all()
    return submissions