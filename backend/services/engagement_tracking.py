import numpy as np
from sqlalchemy.orm import Session
import schemas
import models
from datetime import datetime, timedelta

def calculate_confusion_index(student_id: int, project_id: int, db: Session) -> float:
    """
    Calculate confusion index for a student working on a project using statistical analysis.
    """
    # Get recent engagement logs for this student and project
    recent_logs = db.query(models.EngagementLogs).filter(
        models.EngagementLogs.student_id == student_id,
        models.EngagementLogs.project_id == project_id,
        models.EngagementLogs.timestamp >= datetime.utcnow() - timedelta(hours=1)
    ).all()
    
    if not recent_logs:
        return 0.0
    
    # Extract engagement values
    values = [log.value for log in recent_logs]
    
    # Calculate statistical measures
    mean_value = np.mean(values)
    std_value = np.std(values) if len(values) > 1 else 0
    
    # Confusion indicators:
    # 1. Low engagement values (below mean - 0.5 * std)
    # 2. High variability (std > threshold)
    # 3. Decreasing trend
    
    # Calculate confusion score (0-100)
    confusion_score = 0.0
    
    # Indicator 1: Low engagement
    low_threshold = mean_value - 0.5 * std_value if std_value > 0 else mean_value * 0.7
    low_engagement_count = sum(1 for v in values if v < low_threshold)
    low_engagement_ratio = low_engagement_count / len(values)
    confusion_score += low_engagement_ratio * 30
    
    # Indicator 2: High variability
    if std_value > 0 and mean_value > 0:
        cv = std_value / mean_value  # Coefficient of variation
        if cv > 0.5:  # High variability threshold
            confusion_score += min(30, cv * 20)
    
    # Indicator 3: Decreasing trend (simple linear regression slope)
    if len(values) > 2:
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]  # Slope of trend line
        if slope < 0:  # Decreasing trend
            confusion_score += min(20, abs(slope) * 10)
    
    # Metadata-based confusion indicators
    high_confusion_indicators = 0
    for log in recent_logs:
        if log.metadata_json:
            try:
                metadata = json.loads(log.metadata_json)
                if metadata.get("confusion_flag", False):
                    high_confusion_indicators += 1
            except:
                pass
    
    if high_confusion_indicators > 0:
        confusion_score += min(20, high_confusion_indicators * 5)
    
    return min(100.0, confusion_score)

def detect_engagement_patterns(student_id: int, db: Session) -> dict:
    """
    Detect patterns in student engagement over time.
    """
    # Get all engagement logs for this student
    all_logs = db.query(models.EngagementLogs).filter(
        models.EngagementLogs.student_id == student_id
    ).order_by(models.EngagementLogs.timestamp).all()
    
    if not all_logs:
        return {
            "activity_level": "inactive",
            "consistency": 0.0,
            "peak_hours": [],
            "engagement_trend": "stable"
        }
    
    # Group by hour of day
    hourly_activity = {}
    for log in all_logs:
        hour = log.timestamp.hour
        if hour not in hourly_activity:
            hourly_activity[hour] = 0
        hourly_activity[hour] += 1
    
    # Find peak hours (top 3)
    sorted_hours = sorted(hourly_activity.items(), key=lambda x: x[1], reverse=True)
    peak_hours = [hour for hour, count in sorted_hours[:3]]
    
    # Calculate consistency (ratio of active days to total days)
    if len(all_logs) > 1:
        first_day = all_logs[0].timestamp.date()
        last_day = all_logs[-1].timestamp.date()
        total_days = (last_day - first_day).days + 1
        active_days = len(set(log.timestamp.date() for log in all_logs))
        consistency = active_days / total_days if total_days > 0 else 0
    else:
        consistency = 1.0
    
    # Determine activity level
    total_engagement = sum(log.value for log in all_logs)
    avg_daily_engagement = total_engagement / len(set(log.timestamp.date() for log in all_logs)) if all_logs else 0
    
    if avg_daily_engagement > 50:
        activity_level = "high"
    elif avg_daily_engagement > 20:
        activity_level = "medium"
    else:
        activity_level = "low"
    
    # Determine engagement trend
    if len(all_logs) > 5:
        # Compare first half to second half
        mid_point = len(all_logs) // 2
        first_half_avg = np.mean([log.value for log in all_logs[:mid_point]])
        second_half_avg = np.mean([log.value for log in all_logs[mid_point:]])
        
        if second_half_avg > first_half_avg * 1.2:
            trend = "increasing"
        elif second_half_avg < first_half_avg * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "stable"
    
    return {
        "activity_level": activity_level,
        "consistency": round(consistency, 2),
        "peak_hours": peak_hours,
        "engagement_trend": trend
    }

def log_engagement(engagement: schemas.EngagementLogCreate, db: Session):
    """
    Log student engagement with advanced analytics and confusion detection.
    """
    # Create engagement log entry
    db_engagement = models.EngagementLogs(**engagement.dict())
    db.add(db_engagement)
    db.commit()
    db.refresh(db_engagement)
    
    # Calculate confusion index
    confusion_index = 0.0
    if engagement.project_id:
        confusion_index = calculate_confusion_index(engagement.student_id, engagement.project_id, db)
    
    # Detect engagement patterns
    patterns = detect_engagement_patterns(engagement.student_id, db)
    
    # Print engagement details for demo
    print(f"Logged engagement: Student {engagement.student_id} engaged in {engagement.engagement_type} "
          f"with value {engagement.value}")
    print(f"Confusion Index: {confusion_index:.2f}")
    print(f"Engagement Patterns: {patterns}")
    
    # In a real implementation, this would:
    # 1. Trigger real-time alerts for teachers if confusion index is high
    # 2. Adjust difficulty of content based on engagement patterns
    # 3. Award XP based on engagement quality and duration
    # 4. Update student profiles with engagement insights