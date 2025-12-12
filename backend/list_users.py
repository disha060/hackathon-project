from database import SessionLocal
import models

def list_users():
    db = SessionLocal()
    try:
        users = db.query(models.Users).all()
        if not users:
            print("No users found in the database.")
            return
            
        print(f"\n{'ID':<5} | {'Role':<10} | {'Name':<20} | {'Email'}")
        print("-" * 70)
        for u in users:
            role_str = u.role.value if hasattr(u.role, 'value') else str(u.role)
            print(f"{u.id:<5} | {role_str:<10} | {u.name:<20} | {u.email}")
        print("-" * 70)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    list_users()