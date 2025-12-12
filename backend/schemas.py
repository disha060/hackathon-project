from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# Enums
class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"

class EngagementType(str, Enum):
    PROJECT_WORK = "project_work"
    ASSIGNMENT = "assignment"
    DISCUSSION = "discussion"

class AssignmentStatus(str, Enum):
    ASSIGNED = "assigned"
    SUBMITTED = "submitted"
    GRADED = "graded"

# Base Models
class UserBase(BaseModel):
    name: str
    email: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

class ConceptBase(BaseModel):
    name: str
    description: str

class ConceptCreate(ConceptBase):
    pass

class ConceptResponse(ConceptBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentMasteryBase(BaseModel):
    student_id: int
    concept_id: int
    mastery_score: float = Field(ge=0, le=100)

class StudentMasteryCreate(StudentMasteryBase):
    pass

class StudentMasteryResponse(StudentMasteryBase):
    class Config:
        from_attributes = True

class AssignmentBase(BaseModel):
    concept_id: int
    difficulty_level: int = Field(ge=1, le=5)
    content_url: Optional[str]
    title: str
    description: str

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentAssignmentBase(BaseModel):
    student_id: int
    assignment_id: int
    status: AssignmentStatus = AssignmentStatus.ASSIGNED
    score: Optional[float] = Field(None, ge=0, le=100)

class StudentAssignmentCreate(StudentAssignmentBase):
    pass

class StudentAssignmentResponse(StudentAssignmentBase):
    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str
    teacher_id: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    
    class Config:
        from_attributes = True

class ProjectTeamBase(BaseModel):
    project_id: int
    student_id: int
    role: str

class ProjectTeamCreate(ProjectTeamBase):
    pass

class ProjectTeamResponse(ProjectTeamBase):
    class Config:
        from_attributes = True

class EngagementLogBase(BaseModel):
    student_id: int
    project_id: Optional[int]
    engagement_type: EngagementType
    value: float
    metadata_json: Optional[str]

class EngagementLogCreate(EngagementLogBase):
    pass

class EngagementLogResponse(EngagementLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class SoftSkillScoreBase(BaseModel):
    student_id: int
    skill: str
    score: float = Field(ge=0, le=100)
    evaluator_id: int

class SoftSkillScoreCreate(SoftSkillScoreBase):
    pass

class SoftSkillScoreResponse(SoftSkillScoreBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentXPBase(BaseModel):
    student_id: int
    total_xp: int = 0
    weekly_xp: int = 0

class StudentXPCreate(StudentXPBase):
    pass

class StudentXPResponse(StudentXPBase):
    last_updated: datetime
    
    class Config:
        from_attributes = True

class StudentStreakBase(BaseModel):
    student_id: int
    current_streak: int = 0
    longest_streak: int = 0

class StudentStreakCreate(StudentStreakBase):
    pass

class StudentStreakResponse(StudentStreakBase):
    last_active_date: datetime
    
    class Config:
        from_attributes = True

class StudentBadgeBase(BaseModel):
    student_id: int
    badge_name: str

class StudentBadgeCreate(StudentBadgeBase):
    pass

class StudentBadgeResponse(StudentBadgeBase):
    id: int
    date_awarded: datetime
    
    class Config:
        from_attributes = True

class ConceptProgressBase(BaseModel):
    student_id: int
    concept_id: int
    mastery_score: float = Field(ge=0, le=100)
    level: int = 1

class ConceptProgressCreate(ConceptProgressBase):
    pass

class ConceptProgressResponse(ConceptProgressBase):
    id: int
    
    class Config:
        from_attributes = True

class TeacherInterventionBase(BaseModel):
    teacher_id: int
    student_id: int
    concept_id: Optional[int]
    message: str
    action_taken: str

class TeacherInterventionCreate(TeacherInterventionBase):
    pass

class TeacherInterventionResponse(TeacherInterventionBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Additional Response Models for APIs
class MasteryResponse(BaseModel):
    concept_id: int
    concept_name: str
    mastery_score: float
    level: int
    
    class Config:
        from_attributes = True

class AdaptiveAssignmentResponse(BaseModel):
    assignment_id: int
    title: str
    description: str
    difficulty_level: int
    estimated_time: int  # in minutes
    
    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    student_id: int
    student_name: str
    total_xp: int
    rank: int
    
    class Config:
        from_attributes = True

class BadgeDisplay(BaseModel):
    badge_name: str
    date_awarded: datetime
    
    class Config:
        from_attributes = True

class AIGeneratedAssignment(BaseModel):
    concept_id: int
    title: str
    description: str
    difficulty_level: int
    estimated_time: int  # in minutes
    learning_objectives: List[str]
    
    class Config:
        from_attributes = True

class AIGeneratedProject(BaseModel):
    title: str
    description: str
    skill_area: str
    duration_hours: int
    team_size: int
    learning_outcomes: List[str]
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    role: UserRole

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    notification_type: str
    metadata: Dict[str, Any]
    is_read: bool
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AssignmentCreateWithClasses(BaseModel):
    title: str
    description: str
    concept_id: int
    difficulty_level: int
    content_url: Optional[str] = None
    class_ids: List[int]
    due_date: Optional[datetime] = None
    max_score: Optional[int] = 100

class ClassSimple(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class AssignmentWithClassesResponse(AssignmentResponse):
    classes: List[ClassSimple] = []
    class Config:
        from_attributes = True

# Class Management Schemas
class ClassBase(BaseModel):
    name: str
    description: Optional[str]
    teacher_id: int

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ClassEnrollmentBase(BaseModel):
    class_id: int
    student_id: int

class ClassEnrollmentCreate(BaseModel):
    student_id: int

class ClassEnrollmentResponse(ClassEnrollmentBase):
    id: int
    enrolled_at: datetime
    
    class Config:
        from_attributes = True

class ClassProjectAssignment(BaseModel):
    project_id: int

class ClassAssignmentAssignment(BaseModel):
    assignment_id: int
    due_date: Optional[datetime] = None

class AssignmentSubmissionBase(BaseModel):
    assignment_id: int
    student_id: int
    submission_url: str
    submission_notes: Optional[str] = None

class AssignmentSubmissionCreate(AssignmentSubmissionBase):
    pass

class AssignmentSubmissionResponse(AssignmentSubmissionBase):
    id: int
    submitted_at: datetime
    status: AssignmentStatus = AssignmentStatus.SUBMITTED
    
    class Config:
        from_attributes = True

class ClassAssignmentResponse(AssignmentResponse):
    due_date: Optional[datetime] = None
    assigned_at: datetime
    class_id: int
    
    class Config:
        from_attributes = True

class StudentAssignmentDetail(AssignmentResponse):
    status: AssignmentStatus
    score: Optional[float] = None
    submitted_at: Optional[datetime] = None
    due_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# AI Quiz Generation Schemas
class QuizQuestion(BaseModel):
    id: int
    type: str
    question: str
    options: Optional[List[str]]
    correct_answer: str
    
    class Config:
        from_attributes = True

class GeneratedQuiz(BaseModel):
    topic: str
    difficulty: int
    questions: List[QuizQuestion]
    
    class Config:
        from_attributes = True
