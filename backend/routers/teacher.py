from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas
import models
import database
from services import ai_content_generation, teacher_interventions
import asyncio

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
def create_assignment(assignments: List[schemas.AssignmentCreate], db: Session = Depends(get_db)):
    # Teacher selects AI-generated assignment(s) to assign
    created_assignments = []
    for assignment in assignments:
        db_assignment = models.Assignments(**assignment.dict())
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        created_assignments.append(db_assignment)
    
    return {"message": f"Created {len(created_assignments)} assignments", "assignments": created_assignments}

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
    # Generate quiz questions based on topic using AI
    prompt = f"""
    You are an educational AI that creates quiz questions. Generate {question_count} quiz questions about {topic} at difficulty level {difficulty}/5.
    
    CRITICAL INSTRUCTIONS - READ CAREFULLY:
    1. Mix of question types: Multiple Choice, True/False, Short Answer, Fill in the Blank
    2. Questions should assess understanding, not just memorization
    3. Include plausible distractors for multiple choice questions
    4. Provide correct answers
    5. YOU MUST RESPOND WITH ONLY VALID JSON AND NOTHING ELSE
    6. Format the response EXACTLY as follows:
    {{
        "topic": "{topic}",
        "difficulty": {difficulty},
        "questions": [
            {{
                "id": 1,
                "type": "Multiple Choice",
                "question": "Question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Correct option"
            }}
        ]
    }}
    
    Begin your response with {{ and end with }}. Do not include any other text, explanations, or markdown formatting.
    """
    
    try:
        # Call Gemini API
        response = await ai_content_generation.call_gemini_api(prompt, api_key)
        
        # Parse the response to create QuizQuestion objects
        questions = []
        for i, q in enumerate(response.get("questions", [])):
            questions.append(schemas.QuizQuestion(
                id=i+1,
                type=q.get("type", "Multiple Choice"),
                question=q.get("question", ""),
                options=q.get("options", None),
                correct_answer=q.get("correct_answer", "")
            ))
        
        return schemas.GeneratedQuiz(
            topic=response.get("topic", topic),
            difficulty=response.get("difficulty", difficulty),
            questions=questions
        )
    except Exception as e:
        # Fallback to template-based generation
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
                    correct_answer=f"Aspect {i+1}B"
                ))
            elif question_type == 'True or False':
                questions.append(schemas.QuizQuestion(
                    id=i+1,
                    type=question_type,
                    question=f"{topic} is an important subject.",
                    options=None,
                    correct_answer="True"
                ))
            else:
                questions.append(schemas.QuizQuestion(
                    id=i+1,
                    type=question_type,
                    question=f"Explain a key concept of {topic}.",
                    options=None,
                    correct_answer=f"Key concept explanation for {topic}"
                ))
        
        return schemas.GeneratedQuiz(
            topic=topic,
            difficulty=difficulty,
            questions=questions
        )

@router.get("/interventions", response_model=List[schemas.TeacherInterventionResponse])
def get_interventions(teacher_id: int, db: Session = Depends(get_db)):
    # View all interventions for students
    interventions = db.query(models.TeacherInterventions).filter(
        models.TeacherInterventions.teacher_id == teacher_id
    ).all()
    
    return interventions