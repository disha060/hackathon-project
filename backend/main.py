from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import uvicorn
import os
from typing import Optional
import jwt
from datetime import datetime, timedelta

# Import models and database
import models
import database
from database import get_db

# Import routers
from routers import auth, student, teacher, classes, notifications

# Import auth utilities
from auth_utils import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, get_current_user, get_current_teacher, get_current_student

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI app
app = FastAPI(title="EduAI Platform API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(teacher.router, prefix="", tags=["teacher"])
app.include_router(student.router, prefix="", tags=["student"])
app.include_router(notifications.router, prefix="", tags=["notifications"])
app.include_router(classes.router, prefix="", tags=["classes"])

@app.get("/")
async def root():
    return {"message": "Welcome to the EduAI Platform API! Visit /docs for API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)