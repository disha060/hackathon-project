from database import SessionLocal
import models

def clear_data():
    db = SessionLocal()
    try:
        print("Clearing database...")
        
        # Delete in order of dependencies (child tables first)
        
        # Class related
        db.query(models.ClassAssignments).delete()
        db.query(models.ClassProjects).delete()
        db.query(models.ClassEnrollments).delete()
        db.query(models.Classes).delete()
        
        # Engagement & Gamification
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
        
        # Notifications
        db.query(models.Notification).delete()
        
        # Users
        db.query(models.Users).delete()
        
        db.commit()
        print("All data cleared successfully. You can now register new users via the frontend.")
    except Exception as e:
        print(f"Error clearing data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_data()