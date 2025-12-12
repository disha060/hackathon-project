from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas
database = __import__('database', fromlist=['get_db'])
from services.notification_service import NotificationService
from middleware.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[schemas.NotificationResponse])
async def get_notifications(
    skip: int = 0, 
    limit: int = 10,
    unread: bool = False,
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Get notifications for the current user
    """
    query = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    )
    
    if unread:
        query = query.filter(models.Notification.is_read == False)
        
    notifications = query.offset(skip).limit(limit).all()
    return notifications

@router.get("/{notification_id}", response_model=schemas.NotificationResponse)
async def get_notification(
    notification_id: int,
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Get a specific notification by ID
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    return notification

@router.post("/{notification_id}/read", response_model=schemas.NotificationResponse)
async def mark_as_read(
    notification_id: int,
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Mark a notification as read
    """
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
        
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    db.refresh(notification)
    
    return notification

@router.post("/read-all", response_model=List[schemas.NotificationResponse])
async def mark_all_as_read(
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Mark all notifications as read for the current user
    """
    notifications = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == False
    ).all()
    
    for notification in notifications:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
    
    db.commit()
    
    return notifications

@router.get("/unread/count", response_model=int)
async def get_unread_count(
    current_user: models.Users = Depends(get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Get the count of unread notifications for the current user
    """
    count = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == False
    ).count()
    
    return count
