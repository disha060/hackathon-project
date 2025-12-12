from sqlalchemy.orm import Session
from datetime import datetime
import models
import schemas
from typing import List, Dict, Any

class NotificationService:
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        meta_data: Dict[str, Any] = None
    ) -> models.Notification:
        """
        Create a new notification for a user
        """
        notification = models.Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            meta_data=meta_data or {},
            is_read=False,
            created_at=datetime.utcnow()
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        limit: int = 10,
        unread_only: bool = False
    ) -> List[models.Notification]:
        """
        Get notifications for a user
        """
        query = db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        )
        
        if unread_only:
            query = query.filter(models.Notification.is_read == False)
            
        return query.order_by(models.Notification.created_at.desc()).limit(limit).all()

    @staticmethod
    def mark_as_read(
        db: Session,
        notification_id: int,
        user_id: int
    ) -> models.Notification:
        """
        Mark a notification as read
        """
        notification = db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            db.commit()
            db.refresh(notification)
            
        return notification

    @staticmethod
    def notify_assignment_submission(
        db: Session,
        assignment_id: int,
        student_id: int,
        teacher_id: int
    ) -> models.Notification:
        """
        Notify teacher about a new assignment submission
        """
        assignment = db.query(models.Assignments).filter(
            models.Assignments.id == assignment_id
        ).first()
        
        student = db.query(models.Users).filter(
            models.Users.id == student_id
        ).first()
        
        if not assignment or not student:
            return None
            
        title = "New Assignment Submission"
        message = f"{student.name} has submitted the assignment: {assignment.title}"
        
        return NotificationService.create_notification(
            db=db,
            user_id=teacher_id,
            title=title,
            message=message,
            notification_type="assignment_submission",
            metadata={
                "assignment_id": assignment_id,
                "student_id": student_id,
                "submitted_at": datetime.utcnow().isoformat()
            }
        )
