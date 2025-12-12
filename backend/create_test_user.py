import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from models import Base, Users
from auth_utils import pwd_context

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./amep.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(Users).filter(Users.email == "test@example.com").first()
        if user:
            print("Test user already exists")
            return
            
        # Create test user
        hashed_password = pwd_context.hash("testpassword")
        test_user = Users(
            name="Test User",
            email="test@example.com",
            password_hash=hashed_password,
            role="teacher"
        )
        
        db.add(test_user)
        db.commit()
        print("Test user created successfully!")
        print("Email: test@example.com")
        print("Password: testpassword")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
