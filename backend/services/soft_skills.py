from sqlalchemy.orm import Session
from typing import List
import schemas
import models

def normalize_scores(scores: List[float]) -> List[float]:
    """
    Normalize peer/teacher scores to 0-100 scale.
    For demo purposes, we'll apply a simple normalization.
    """
    # In a real implementation, this would:
    # 1. Apply statistical normalization techniques
    # 2. Handle outliers and inconsistent scoring
    # 3. Ensure fair comparison across different evaluators
    
    if not scores:
        return []
    
    min_score = min(scores)
    max_score = max(scores)
    
    if min_score == max_score:
        return [50.0] * len(scores)  # If all scores are the same, map to middle value
    
    normalized = [((score - min_score) / (max_score - min_score)) * 100 for score in scores]
    return normalized

def calculate_average_soft_skill_score(student_id: int, skill: str, db: Session) -> float:
    """
    Calculate average score for a specific soft skill for a student.
    For demo purposes, we'll return a mock value.
    """
    # In a real implementation, this would:
    # 1. Query all scores for the student and skill
    # 2. Apply normalization
    # 3. Calculate weighted average
    
    import random
    return random.uniform(70, 95)