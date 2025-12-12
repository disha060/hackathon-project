from database import SessionLocal
import models

def list_students():
    db = SessionLocal()
    try:
        students = db.query(models.Users).filter(models.Users.role == "student").all()
        if not students:
            print("No students found in the database.")
            return
            
        print(f"\n{'ID':<5} | {'Name':<20} | {'Email'}")
        print("-" * 50)
        for s in students:
            print(f"{s.id:<5} | {s.name:<20} | {s.email}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_students()