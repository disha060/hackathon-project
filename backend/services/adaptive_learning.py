import numpy as np
from sqlalchemy.orm import Session
from typing import List
import schemas
import models

class BayesianKnowledgeTracer:
    def __init__(self, init_prior=0.5, learn_rate=0.3, guess_rate=0.1, slip_rate=0.1):
        self.init_prior = init_prior
        self.learn_rate = learn_rate
        self.guess_rate = guess_rate
        self.slip_rate = slip_rate
    
    def update_mastery(self, prev_mastery, correctness):
        """
        Update mastery probability using Bayesian Knowledge Tracing
        """
        # Probability of getting question right given knowledge
        p_correct_given_knowledge = 1 - self.slip_rate
        
        # Probability of getting question right given no knowledge
        p_correct_given_no_knowledge = self.guess_rate
        
        # Update using Bayes' theorem
        if correctness:
            # Correct answer
            numerator = prev_mastery * p_correct_given_knowledge
            denominator = (prev_mastery * p_correct_given_knowledge) + ((1 - prev_mastery) * p_correct_given_no_knowledge)
        else:
            # Incorrect answer
            numerator = prev_mastery * (1 - p_correct_given_knowledge)
            denominator = (prev_mastery * (1 - p_correct_given_knowledge)) + ((1 - prev_mastery) * (1 - p_correct_given_no_knowledge))
        
        if denominator == 0:
            return prev_mastery
            
        new_mastery = numerator / denominator
        # Apply learning rate
        new_mastery = min(1.0, new_mastery + self.learn_rate * (1 - new_mastery))
        
        return new_mastery

# Initialize BKT model
bkt_model = BayesianKnowledgeTracer()

def get_adaptive_assignments(student_id: int, db: Session) -> List[schemas.AdaptiveAssignmentResponse]:
    """
    Get adaptive assignments based on student's mastery levels using BKT model.
    """
    # Get student's current mastery levels
    mastery_records = db.query(models.StudentMastery).filter(
        models.StudentMastery.student_id == student_id
    ).all()
    
    # For demo, we'll return assignments based on lowest mastery concepts
    assignments = []
    
    if not mastery_records:
        # New student - return beginner assignments
        assignments = [
            schemas.AdaptiveAssignmentResponse(
                assignment_id=1,
                title="Python Basics Starter",
                description="Introduction to variables and data types",
                difficulty_level=1,
                estimated_time=20
            )
        ]
    else:
        # Sort by mastery score to find weakest concepts
        sorted_mastery = sorted(mastery_records, key=lambda x: x.mastery_score)
        weakest_concept = sorted_mastery[0] if sorted_mastery else None
        
        if weakest_concept and weakest_concept.mastery_score < 70:
            # Focus on weak areas
            assignments = [
                schemas.AdaptiveAssignmentResponse(
                    assignment_id=weakest_concept.concept_id * 10 + 1,
                    title=f"Reinforcement: {weakest_concept.concept.name}",
                    description=f"Additional practice for {weakest_concept.concept.name}",
                    difficulty_level=max(1, int(weakest_concept.mastery_score / 20)),
                    estimated_time=30
                )
            ]
        else:
            # Advance to next level
            assignments = [
                schemas.AdaptiveAssignmentResponse(
                    assignment_id=2,
                    title="Intermediate Challenge",
                    description="Apply your knowledge in new contexts",
                    difficulty_level=3,
                    estimated_time=45
                )
            ]
    
    return assignments

def update_mastery_score(student_id: int, concept_id: int, score: float, db: Session):
    """
    Update student's mastery score for a concept after assignment submission using BKT.
    """
    # Get current mastery record
    mastery_record = db.query(models.StudentMastery).filter(
        models.StudentMastery.student_id == student_id,
        models.StudentMastery.concept_id == concept_id
    ).first()
    
    # Convert percentage score to correctness (1 if >= 70%, 0 otherwise)
    correctness = 1 if score >= 70 else 0
    
    if mastery_record:
        # Update existing mastery using BKT
        prev_mastery = mastery_record.mastery_score / 100.0
        new_mastery = bkt_model.update_mastery(prev_mastery, correctness)
        mastery_record.mastery_score = new_mastery * 100
    else:
        # Create new mastery record
        initial_mastery = 0.5 if correctness else 0.2
        new_mastery = bkt_model.update_mastery(initial_mastery, correctness)
        mastery_record = models.StudentMastery(
            student_id=student_id,
            concept_id=concept_id,
            mastery_score=new_mastery * 100
        )
        db.add(mastery_record)
    
    db.commit()
    print(f"Updated mastery for student {student_id} in concept {concept_id} to {new_mastery * 100:.2f}%")

def recommend_learning_path(student_id: int, db: Session) -> List[dict]:
    """
    Recommend a personalized learning path based on student's mastery levels and goals.
    """
    # Get student's current mastery levels
    mastery_records = db.query(models.StudentMastery).filter(
        models.StudentMastery.student_id == student_id
    ).all()
    
    # Get student's concept progress
    progress_records = db.query(models.ConceptProgress).filter(
        models.ConceptProgress.student_id == student_id
    ).all()
    
    # Get all concepts
    all_concepts = db.query(models.Concepts).all()
    
    # Build recommendation
    recommendations = []
    
    if not mastery_records:
        # New student - recommend foundational concepts
        foundational_concepts = [c for c in all_concepts if "basic" in c.name.lower() or "intro" in c.name.lower()]
        if not foundational_concepts:
            foundational_concepts = all_concepts[:3]  # First 3 concepts as fallback
        
        for concept in foundational_concepts:
            recommendations.append({
                "concept_id": concept.id,
                "concept_name": concept.name,
                "reason": "Foundational skill for beginners",
                "priority": "high",
                "estimated_time": 60
            })
    else:
        # Existing student - analyze gaps and suggest next steps
        # 1. Find weak areas (mastery < 70%)
        weak_areas = [m for m in mastery_records if m.mastery_score < 70]
        
        for mastery in weak_areas:
            concept = next((c for c in all_concepts if c.id == mastery.concept_id), None)
            if concept:
                recommendations.append({
                    "concept_id": concept.id,
                    "concept_name": concept.name,
                    "reason": f"Reinforce weak area (current mastery: {mastery.mastery_score:.1f}%)",
                    "priority": "high",
                    "estimated_time": 90
                })
        
        # 2. Find next concepts to learn (prerequisites met)
        mastered_concepts = [m for m in mastery_records if m.mastery_score >= 70]
        mastered_concept_ids = [m.concept_id for m in mastered_concepts]
        
        # Simple prerequisite logic (in a real system, this would be more complex)
        for concept in all_concepts:
            if concept.id not in mastered_concept_ids and concept.id not in [r["concept_id"] for r in recommendations]:
                # Check if prerequisites are met (simplified)
                # In a real system, you'd have a prerequisites table
                prereq_met = True  # Simplified for demo
                
                if prereq_met:
                    recommendations.append({
                        "concept_id": concept.id,
                        "concept_name": concept.name,
                        "reason": "Next logical concept to learn",
                        "priority": "medium",
                        "estimated_time": 120
                    })
        
        # 3. Advanced topics for highly mastered concepts
        advanced_concepts = [m for m in mastery_records if m.mastery_score >= 90]
        
        for mastery in advanced_concepts:
            # Suggest related advanced topics
            related_advanced = [c for c in all_concepts 
                              if c.id != mastery.concept_id and 
                                 c.name.lower().find(mastery.concept.name.lower()[:4]) != -1]
            
            for concept in related_advanced[:2]:  # Max 2 related advanced topics
                if concept.id not in [r["concept_id"] for r in recommendations]:
                    recommendations.append({
                        "concept_id": concept.id,
                        "concept_name": concept.name,
                        "reason": f"Advanced extension of mastered concept ({mastery.mastery_score:.1f}% mastery)",
                        "priority": "low",
                        "estimated_time": 150
                    })
    
    # Sort by priority (high first) then by estimated time
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: (priority_order[x["priority"]], x["estimated_time"]))
    
    return recommendations