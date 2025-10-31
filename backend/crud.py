from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Daily_Activity
from datetime import date, datetime, timezone

def get_activity(
        db: Session,
        name: str,
        day: date,
        count: int,
        notes: str = ""
) -> Daily_Activity:
    """Get existing daily activity if it exists otherwise create new one

    Args:
        db (Session): _description_
        name (str): _description_
        day (date): _description_
        count (int): _description_
        notes (str, optional): _description_. Defaults to "".

    Returns:
        Daily_Activity: model for activity
    """
    activity = db.query(Daily_Activity).filter(
        and_(Daily_Activity.name == name.lower(), Daily_Activity.day == day)
    ).first()

    if activity:
        #Update existing activity if it exists
        activity.count = count
        activity.notes = notes
        activity.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(activity)
        return activity
    else:
        #If activity doesnt exist create new one
        db_activity = Daily_Activity(
            name = name.lower(),
            day = day,
            count = count,
            notes = notes
        )
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity
    
def add_in_activity(
        db: Session,
        name: str,
        day: date,
        addition: int,
        notes: str = ""
):
    """Add an integer value to activity, can be positive or negative.

    Args:
        db (Session): _description_
        name (str): _description_
        day (date): _description_
        addition (int): _description_
        notes (str, optional): _description_. Defaults to "".

    Returns:
        Daily_Activity: _description_
    """
    activity = db.query(Daily_Activity).filter(
        and_(Daily_Activity.name == name.lower(), Daily_Activity.day == day)
    ).first()

    if activity:
        activity.count += addition
        if notes:
            activity.notes = notes
            activity.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(activity)
            return activity
    else:
        return None
