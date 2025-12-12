from database import SessionLocal
import models

def set_teacher_role(email: str):
    db = SessionLocal()
    try:
        user = db.query(models.Users).filter(models.Users.email == email).first()
        if user:
            user.role = models.UserRole.TEACHER
            db.commit()
            print(f"Success: User '{email}' has been updated to role 'teacher'.")
        else:
            print(f"Error: User with email '{email}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    target_email = input("Enter the email address to promote to teacher: ")
    set_teacher_role(target_email)