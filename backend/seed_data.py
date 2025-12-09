import models
import database
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

def seed_database():
    db: Session = database.SessionLocal()
    
    # Clear existing data
    db.query(models.TeacherInterventions).delete()
    db.query(models.StudentBadges).delete()
    db.query(models.StudentStreaks).delete()
    db.query(models.StudentXP).delete()
    db.query(models.SoftSkillScores).delete()
    db.query(models.EngagementLogs).delete()
    db.query(models.ProjectTeams).delete()
    db.query(models.Projects).delete()
    db.query(models.StudentAssignments).delete()
    db.query(models.Assignments).delete()
    db.query(models.ConceptProgress).delete()
    db.query(models.StudentMastery).delete()
    db.query(models.Concepts).delete()
    db.query(models.Users).delete()
    
    # Create sample users (students and teachers)
    students = [
        models.Users(name="Alice Johnson", email="alice@example.com", password_hash="password123", role="student"),
        models.Users(name="Bob Smith", email="bob@example.com", password_hash="password123", role="student"),
        models.Users(name="Carol Davis", email="carol@example.com", password_hash="password123", role="student"),
        models.Users(name="David Wilson", email="david@example.com", password_hash="password123", role="student"),
        models.Users(name="Eva Brown", email="eva@example.com", password_hash="password123", role="student")
    ]
    
    teachers = [
        models.Users(name="Prof. Anderson", email="anderson@university.edu", password_hash="password123", role="teacher"),
        models.Users(name="Dr. Baker", email="baker@university.edu", password_hash="password123", role="teacher")
    ]
    
    # Add users to database
    for student in students:
        db.add(student)
    for teacher in teachers:
        db.add(teacher)
    db.commit()
    
    # Refresh to get IDs
    for student in students:
        db.refresh(student)
    for teacher in teachers:
        db.refresh(teacher)
    
    # Create sample concepts
    concepts = [
        models.Concepts(name="Python Basics", description="Introduction to Python programming language"),
        models.Concepts(name="Data Structures", description="Lists, dictionaries, sets, and tuples in Python"),
        models.Concepts(name="Algorithms", description="Basic algorithms and complexity analysis"),
        models.Concepts(name="Object-Oriented Programming", description="Classes, objects, inheritance, and polymorphism"),
        models.Concepts(name="Database Design", description="Relational database design and SQL")
    ]
    
    # Add concepts to database
    for concept in concepts:
        db.add(concept)
    db.commit()
    
    # Refresh to get IDs
    for concept in concepts:
        db.refresh(concept)
    
    # Create sample mastery data
    mastery_data = [
        models.StudentMastery(student_id=students[0].id, concept_id=concepts[0].id, mastery_score=85.0),
        models.StudentMastery(student_id=students[0].id, concept_id=concepts[1].id, mastery_score=75.0),
        models.StudentMastery(student_id=students[1].id, concept_id=concepts[0].id, mastery_score=90.0),
        models.StudentMastery(student_id=students[1].id, concept_id=concepts[1].id, mastery_score=60.0),
        models.StudentMastery(student_id=students[2].id, concept_id=concepts[0].id, mastery_score=70.0),
        models.StudentMastery(student_id=students[2].id, concept_id=concepts[1].id, mastery_score=80.0),
        models.StudentMastery(student_id=students[3].id, concept_id=concepts[0].id, mastery_score=35.0),  # Struggling student
        models.StudentMastery(student_id=students[4].id, concept_id=concepts[0].id, mastery_score=65.0)
    ]
    
    # Add mastery data to database
    for mastery in mastery_data:
        db.add(mastery)
    db.commit()
    
    # Create sample assignments
    assignments = [
        models.Assignments(concept_id=concepts[0].id, difficulty_level=1, title="Variables and Types", 
                          description="Practice declaring variables and working with different data types"),
        models.Assignments(concept_id=concepts[0].id, difficulty_level=2, title="Control Flow", 
                          description="Practice if statements, loops, and exception handling"),
        models.Assignments(concept_id=concepts[1].id, difficulty_level=2, title="List Operations", 
                          description="Practice creating, accessing, and manipulating lists"),
        models.Assignments(concept_id=concepts[1].id, difficulty_level=3, title="Dictionary Challenges", 
                          description="Practice working with dictionaries and nested data structures")
    ]
    
    # Add assignments to database
    for assignment in assignments:
        db.add(assignment)
    db.commit()
    
    # Refresh to get IDs
    for assignment in assignments:
        db.refresh(assignment)
    
    # Create sample student assignments
    student_assignments = [
        models.StudentAssignments(student_id=students[0].id, assignment_id=assignments[0].id, status="graded", score=90.0),
        models.StudentAssignments(student_id=students[0].id, assignment_id=assignments[1].id, status="graded", score=85.0),
        models.StudentAssignments(student_id=students[1].id, assignment_id=assignments[0].id, status="graded", score=95.0),
        models.StudentAssignments(student_id=students[2].id, assignment_id=assignments[0].id, status="submitted"),
        models.StudentAssignments(student_id=students[3].id, assignment_id=assignments[0].id, status="graded", score=40.0)
    ]
    
    # Add student assignments to database
    for sa in student_assignments:
        db.add(sa)
    db.commit()
    
    # Create sample projects
    projects = [
        models.Projects(title="EcoTracker App", description="Build an application to track and reduce personal carbon footprint",
                       teacher_id=teachers[0].id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=14)),
        models.Projects(title="Community Bulletin Board", description="Create a digital platform for community announcements and events",
                       teacher_id=teachers[1].id, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=21))
    ]
    
    # Add projects to database
    for project in projects:
        db.add(project)
    db.commit()
    
    # Refresh to get IDs
    for project in projects:
        db.refresh(project)
    
    # Create sample project teams
    project_teams = [
        models.ProjectTeams(project_id=projects[0].id, student_id=students[0].id, role="leader"),
        models.ProjectTeams(project_id=projects[0].id, student_id=students[1].id, role="member"),
        models.ProjectTeams(project_id=projects[0].id, student_id=students[2].id, role="member"),
        models.ProjectTeams(project_id=projects[1].id, student_id=students[2].id, role="leader"),
        models.ProjectTeams(project_id=projects[1].id, student_id=students[3].id, role="member"),
        models.ProjectTeams(project_id=projects[1].id, student_id=students[4].id, role="member")
    ]
    
    # Add project teams to database
    for pt in project_teams:
        db.add(pt)
    db.commit()
    
    # Create sample engagement logs
    engagement_logs = [
        models.EngagementLogs(student_id=students[0].id, project_id=projects[0].id, engagement_type="project_work", value=45.5),
        models.EngagementLogs(student_id=students[1].id, project_id=projects[0].id, engagement_type="project_work", value=30.0),
        models.EngagementLogs(student_id=students[2].id, project_id=projects[1].id, engagement_type="assignment", value=20.5)
    ]
    
    # Add engagement logs to database
    for el in engagement_logs:
        db.add(el)
    db.commit()
    
    # Create sample soft skill scores
    soft_skill_scores = [
        models.SoftSkillScores(student_id=students[0].id, skill="communication", score=90.0, evaluator_id=teachers[0].id),
        models.SoftSkillScores(student_id=students[0].id, skill="teamwork", score=85.0, evaluator_id=teachers[0].id),
        models.SoftSkillScores(student_id=students[1].id, skill="communication", score=80.0, evaluator_id=teachers[1].id),
        models.SoftSkillScores(student_id=students[1].id, skill="problem_solving", score=95.0, evaluator_id=teachers[1].id)
    ]
    
    # Add soft skill scores to database
    for ss in soft_skill_scores:
        db.add(ss)
    db.commit()
    
    # Create sample student XP
    student_xps = [
        models.StudentXP(student_id=students[0].id, total_xp=1250, weekly_xp=350),
        models.StudentXP(student_id=students[1].id, total_xp=1100, weekly_xp=300),
        models.StudentXP(student_id=students[2].id, total_xp=950, weekly_xp=200),
        models.StudentXP(student_id=students[3].id, total_xp=400, weekly_xp=100),
        models.StudentXP(student_id=students[4].id, total_xp=750, weekly_xp=150)
    ]
    
    # Add student XP to database
    for sxp in student_xps:
        db.add(sxp)
    db.commit()
    
    # Create sample student streaks
    student_streaks = [
        models.StudentStreaks(student_id=students[0].id, current_streak=7, longest_streak=15),
        models.StudentStreaks(student_id=students[1].id, current_streak=5, longest_streak=10),
        models.StudentStreaks(student_id=students[2].id, current_streak=3, longest_streak=8),
        models.StudentStreaks(student_id=students[3].id, current_streak=1, longest_streak=3),
        models.StudentStreaks(student_id=students[4].id, current_streak=4, longest_streak=6)
    ]
    
    # Add student streaks to database
    for streak in student_streaks:
        db.add(streak)
    db.commit()
    
    # Create sample student badges
    student_badges = [
        models.StudentBadges(student_id=students[0].id, badge_name="First Project Completed"),
        models.StudentBadges(student_id=students[0].id, badge_name="Weeklong Streak"),
        models.StudentBadges(student_id=students[1].id, badge_name="Quiz Master"),
        models.StudentBadges(student_id=students[2].id, badge_name="Team Player")
    ]
    
    # Add student badges to database
    for badge in student_badges:
        db.add(badge)
    db.commit()
    
    # Create sample concept progress
    concept_progress = [
        models.ConceptProgress(student_id=students[0].id, concept_id=concepts[0].id, mastery_score=85.0, level=4),
        models.ConceptProgress(student_id=students[0].id, concept_id=concepts[1].id, mastery_score=75.0, level=3),
        models.ConceptProgress(student_id=students[1].id, concept_id=concepts[0].id, mastery_score=90.0, level=5),
        models.ConceptProgress(student_id=students[2].id, concept_id=concepts[0].id, mastery_score=70.0, level=3)
    ]
    
    # Add concept progress to database
    for cp in concept_progress:
        db.add(cp)
    db.commit()
    
    # Create sample teacher interventions
    interventions = [
        models.TeacherInterventions(teacher_id=teachers[0].id, student_id=students[3].id, concept_id=concepts[0].id,
                                  message="Struggling with basic Python concepts. Recommended additional practice.",
                                  action_taken="Assigned extra exercises")
    ]
    
    # Add interventions to database
    for intervention in interventions:
        db.add(intervention)
    db.commit()
    
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()