import os
import json
import asyncio
from sqlalchemy.orm import Session
from typing import List
import schemas
import models

# Template-based content generation (fallback when API unavailable)
CONTENT_TEMPLATES = {
    "assignment": {
        1: {
            "title": "{concept} Fundamentals Quiz",
            "description": "Test your understanding of basic {concept} concepts including {topics}",
            "objectives": [
                "Identify key {concept} principles",
                "Apply basic {concept} techniques",
                "Solve simple {concept} problems"
            ]
        },
        2: {
            "title": "{concept} Practice Exercises",
            "description": "Practice applying {concept} through hands-on exercises covering {topics}",
            "objectives": [
                "Implement {concept} solutions",
                "Debug common {concept} issues",
                "Optimize {concept} performance"
            ]
        },
        3: {
            "title": "{concept} Advanced Challenges",
            "description": "Tackle complex {concept} problems requiring deep understanding of {topics}",
            "objectives": [
                "Design sophisticated {concept} systems",
                "Analyze {concept} trade-offs",
                "Evaluate {concept} best practices"
            ]
        }
    },
    "project": {
        "app_development": {
            "title": "{skill_area} Application Project",
            "description": "Build a complete {skill_area} application that demonstrates core concepts",
            "outcomes": [
                "Apply {skill_area} design patterns",
                "Implement user authentication",
                "Deploy a production-ready application"
            ]
        },
        "data_analysis": {
            "title": "{skill_area} Analytics Dashboard",
            "description": "Create a dashboard to visualize and analyze {skill_area} data trends",
            "outcomes": [
                "Process large datasets",
                "Create interactive visualizations",
                "Generate actionable insights"
            ]
        }
    }
}

def generate_assignment_prompt(concept_name: str, difficulty: int, topics: List[str]) -> str:
    """Generate prompt for assignment creation"""
    template = CONTENT_TEMPLATES["assignment"].get(difficulty, CONTENT_TEMPLATES["assignment"][2])
    topics_str = ", ".join(topics)
    
    return f"""
    Create a {concept_name} assignment for students.
    
    Title: {template['title'].format(concept=concept_name)}
    Description: {template['description'].format(concept=concept_name, topics=topics_str)}
    Difficulty Level: {difficulty}/5
    Estimated Time: {difficulty * 15 + 10} minutes
    
    Learning Objectives:
    {chr(10).join([f"- {obj.format(concept=concept_name)}" for obj in template['objectives']])}
    
    Please format the response as JSON with the following structure:
    {{
        "title": "Assignment Title",
        "description": "Detailed description",
        "difficulty_level": 1-5,
        "estimated_time": 15,
        "learning_objectives": ["objective1", "objective2", "objective3"]
    }}
    """

def generate_project_prompt(skill_area: str, project_type: str) -> str:
    """Generate prompt for project creation"""
    template = CONTENT_TEMPLATES["project"].get(project_type, CONTENT_TEMPLATES["project"]["app_development"])
    
    return f"""
    Create a {skill_area} project idea for students.
    
    Title: {template['title'].format(skill_area=skill_area)}
    Description: {template['description'].format(skill_area=skill_area)}
    Duration: {20 + len(skill_area) * 2} hours
    Team Size: {3 if 'app' in project_type else 4} members
    
    Learning Outcomes:
    {chr(10).join([f"- {outcome.format(skill_area=skill_area)}" for outcome in template['outcomes']])}
    
    Please format the response as JSON with the following structure:
    {{
        "title": "Project Title",
        "description": "Detailed description",
        "duration_hours": 20,
        "team_size": 3,
        "learning_outcomes": ["outcome1", "outcome2", "outcome3"]
    }}
    """

async def call_gemini_api(prompt: str, api_key: str = None) -> dict:
    """Call Gemini API to generate content"""
    # Check if API key is provided
    if not api_key and "GEMINI_API_KEY" not in os.environ:
        # No API key available, return simulated response
        return simulate_gemini_response(prompt)
    
    # Use provided API key or environment variable
    api_key = api_key or os.environ["GEMINI_API_KEY"]
    
    # In a real implementation, this would make an actual API call
    # For demo purposes, we'll simulate the response
    print("Using Gemini API for content generation...")
    
    # Simulate API delay
    await asyncio.sleep(1)
    
    # Return simulated response based on prompt content
    return simulate_gemini_response(prompt)

def simulate_gemini_response(prompt: str) -> dict:
    """Simulate Gemini API response for demo purposes"""
    if "assignment" in prompt.lower():
        return {
            "title": "AI-Generated Assignment",
            "description": "This assignment was intelligently generated using advanced AI models to match your learning objectives",
            "difficulty_level": 3,
            "estimated_time": 45,
            "learning_objectives": [
                "Demonstrate understanding of core concepts",
                "Apply knowledge to solve practical problems",
                "Develop critical thinking skills"
            ]
        }
    else:
        return {
            "title": "AI-Generated Project",
            "description": "This project was designed using cutting-edge AI to provide an engaging learning experience",
            "duration_hours": 30,
            "team_size": 4,
            "learning_outcomes": [
                "Synthesize knowledge across multiple domains",
                "Collaborate effectively in team environments",
                "Create innovative solutions to real-world problems"
            ]
        }

def generate_assignments(concept_id: int, db: Session, api_key: str = None) -> List[schemas.AIGeneratedAssignment]:
    """
    Generate AI-suggested assignments for a concept using Gemini API or templates.
    """
    # Get concept details
    concept = db.query(models.Concepts).filter(models.Concepts.id == concept_id).first()
    if not concept:
        # Fallback to template-based generation
        template = CONTENT_TEMPLATES["assignment"][2]  # Medium difficulty
        assignments = [
            schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=template["title"].format(concept="Programming"),
                description=template["description"].format(concept="Programming", topics="fundamentals"),
                difficulty_level=2,
                estimated_time=40,
                learning_objectives=template["objectives"]
            )
        ]
        return assignments
    
    # Generate assignments for different difficulty levels
    assignments = []
    topics = ["basics", "intermediate", "advanced"]
    
    for difficulty in [1, 2, 3]:
        # Try to call Gemini API
        prompt = generate_assignment_prompt(concept.name, difficulty, topics[:difficulty])
        
        try:
            # Call Gemini API with fallback
            response = asyncio.run(call_gemini_api(prompt, api_key))
            
            assignment = schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=response["title"],
                description=response["description"],
                difficulty_level=response["difficulty_level"],
                estimated_time=response["estimated_time"],
                learning_objectives=response["learning_objectives"]
            )
            assignments.append(assignment)
        except Exception as e:
            # Fallback to template-based generation
            template = CONTENT_TEMPLATES["assignment"].get(difficulty, CONTENT_TEMPLATES["assignment"][2])
            fallback_assignment = schemas.AIGeneratedAssignment(
                concept_id=concept_id,
                title=template["title"].format(concept=concept.name),
                description=template["description"].format(concept=concept.name, topics=", ".join(topics[:difficulty])),
                difficulty_level=difficulty,
                estimated_time=difficulty * 15 + 10,
                learning_objectives=[obj.format(concept=concept.name) for obj in template["objectives"]]
            )
            assignments.append(fallback_assignment)
    
    return assignments

def generate_projects(skill_area: str, db: Session, api_key: str = None) -> List[schemas.AIGeneratedProject]:
    """
    Generate AI-suggested projects for a skill area using Gemini API or templates.
    """
    projects = []
    project_types = ["app_development", "data_analysis"]
    
    for project_type in project_types:
        # Try to call Gemini API
        prompt = generate_project_prompt(skill_area, project_type)
        
        try:
            # Call Gemini API with fallback
            response = asyncio.run(call_gemini_api(prompt, api_key))
            
            project = schemas.AIGeneratedProject(
                title=response["title"],
                description=response["description"],
                skill_area=skill_area,
                duration_hours=response["duration_hours"],
                team_size=response["team_size"],
                learning_outcomes=response["learning_outcomes"]
            )
            projects.append(project)
        except Exception as e:
            # Fallback to template-based generation
            template = CONTENT_TEMPLATES["project"].get(project_type, CONTENT_TEMPLATES["project"]["app_development"])
            fallback_project = schemas.AIGeneratedProject(
                title=template["title"].format(skill_area=skill_area),
                description=template["description"].format(skill_area=skill_area),
                skill_area=skill_area,
                duration_hours=20 + len(skill_area) * 2,
                team_size=3 if 'app' in project_type else 4,
                learning_outcomes=[outcome.format(skill_area=skill_area) for outcome in template["outcomes"]]
            )
            projects.append(fallback_project)
    
    return projects