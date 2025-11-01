from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Daily_Activity
from datetime import date, datetime, timezone, timedelta


def get_activity(
    db: Session, name: str, day: date, count: int, notes: str = ""
) -> Daily_Activity | None :
    """Get existing daily activity if it exists otherwise return None

    Args:
        db (Session): _description_
        name (str): _description_
        day (date): _description_
        count (int): _description_
        notes (str, optional): _description_. Defaults to "".

    Returns:
        Daily_Activity: model for activity
    """
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == name.lower(), Daily_Activity.day == day))
        .first()
    )

    if activity:
        # Update existing activity if it exists
        activity.count = count
        activity.notes = notes
        activity.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(activity)
        return activity
    else:
        return None
        # If activity doesnt exist return None

def create_activity(
    db: Session, name: str, day: date, count: int, notes: str = ""
) -> Daily_Activity:
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == name.lower(), Daily_Activity.day == day))
        .first()
    )
    if activity:
        # Return activity if it already exists
        return activity
    else:
        # If activity doesnt exist create activity
        db_activity = Daily_Activity(
            name=name.lower(), day=day, count=count, notes=notes
        )
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity

def add_in_activity(
    db: Session, name: str, day: date, addition: int, notes: str = ""
) -> Daily_Activity | None:
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
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == name.lower(), Daily_Activity.day == day))
        .first()
    )

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


def get_daily_acitivies(db: Session, days_back: int) -> list[Daily_Activity]:
    cutoff = date.today() - timedelta(days=days_back)
    return (
        db.query(Daily_Activity)
        .filter(Daily_Activity.day >= cutoff)
        .order_by(Daily_Activity.day.desc(), Daily_Activity.name)
        .all()
    )


def get_activity_summary(
    db: Session, activity_name: str
) -> list[Daily_Activity] | None:
    query = db.query(Daily_Activity)
    if activity_name:
        query = query.filter(Daily_Activity.name == activity_name.lower())
        return query.order_by(Daily_Activity).all()
    else:
        return None
