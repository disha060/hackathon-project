from sqlalchemy.orm import Session
from typing import List, Dict
import schemas
import models

def detect_struggling_students(teacher_id: int, db: Session) -> List[Dict]:
    """
    Identify students who need intervention based on mastery scores or confusion index.
    For demo purposes, we'll return mock data.
    """
    # In a real implementation, this would:
    # 1. Query students with low mastery scores
    # 2. Check confusion index from engagement tracking
    # 3. Identify patterns indicating struggle
    # 4. Prioritize students for teacher intervention
    
    struggling_students = [
        {
            "student_id": 3,
            "student_name": "David Wilson",
            "issue": "Low mastery score in Python Basics",
            "mastery_score": 35.0,
            "recommended_action": "Assign additional practice exercises"
        },
        {
            "student_id": 5,
            "student_name": "Eva Brown",
            "issue": "High confusion index in Data Structures project",
            "confusion_index": 85.5,
            "recommended_action": "Schedule one-on-one meeting"
        }
    ]
    
    return struggling_students

def get_class_dashboard(teacher_id: int, db: Session) -> Dict:
    """
    Get class-wide dashboard with mastery, engagement, soft skills, and leaderboard data.
    For demo purposes, we'll return mock data.
    """
    # In a real implementation, this would:
    # 1. Aggregate mastery data for all students
    # 2. Compile engagement metrics
    # 3. Summarize soft skill assessments
    # 4. Generate leaderboard
    
    dashboard = {
        "class_mastery_summary": {
            "Python Basics": {"average": 72.5, "median": 75.0},
            "Data Structures": {"average": 65.0, "median": 68.0},
            "Algorithms": {"average": 58.0, "median": 60.0}
        },
        "engagement_metrics": {
            "active_students": 18,
            "avg_daily_engagement": 45.5,
            "high_confusion_cases": 3
        },
        "soft_skill_summary": {
            "communication": {"average": 82.0},
            "teamwork": {"average": 78.5},
            "problem_solving": {"average": 85.0}
        },
        "leaderboard": [
            {"student_id": 1, "student_name": "Alice Johnson", "total_xp": 1250},
            {"student_id": 2, "student_name": "Bob Smith", "total_xp": 1100},
            {"student_id": 3, "student_name": "Carol Davis", "total_xp": 950}
        ],
        "struggling_students": detect_struggling_students(teacher_id, db)
    }
    
    return dashboard