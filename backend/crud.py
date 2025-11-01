from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Daily_Activity
from datetime import date, datetime, timezone, timedelta
import schemas


def get_activity(db: Session, name: str) -> Daily_Activity | None:
    """Get an activity by name

    Args:
        db (Session): database session to run query on
        name (str): name of activity to query

    Returns:
        Daily_Activity | None: returns activity if found else None
    """
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == name.lower()))
        .first()
    )

    if activity:
        # Update existing activity if it exists
        return activity
    else:
        return None
        # If activity doesnt exist return None


def create_activity(
    db: Session, created_activity: schemas.DailyActivityCreate
) -> Daily_Activity:
    """Create a new actiivty

    Args:
        db (Session): database session to run query on
        created_activity (schemas.DailyActivityCreate): input data to create activity

    Returns:
        Daily_Activity: returns activity created
    """
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == created_activity.name.lower()))
        .first()
    )
    if activity:
        # Return activity if it already exists
        return activity
    else:
        # If activity doesnt exist create activity
        db_activity = Daily_Activity(
            name=created_activity.name.lower(), count=0, notes=""
        )
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity


def add_in_activity(
    db: Session,
    updated_activity: schemas.DailyActivityUpdate,
) -> Daily_Activity | None:
    """Add an integer value to activity, can be positive or negative.

    Args:
        db (Session): _description_
        updated_activity (schemas.DailyActivityUpdate): _description_

    Returns:
        Daily_Activity | None: _description_
    """
    activity = (
        db.query(Daily_Activity)
        .filter(and_(Daily_Activity.name == updated_activity.name.lower()))
        .first()
    )

    if activity:
        activity.count += updated_activity.addition
        if updated_activity.notes is not None:
            activity.notes = updated_activity.notes
        activity.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(activity)
        return activity
    else:
        return None


def get_daily_acitivies(db: Session, days_back: int) -> list[Daily_Activity]:
    """Get list of daily activities up to a amount of days back

    Args:
        db (Session): database session to run query on
        days_back (int): amount of days to search back to

    Returns:
        list[Daily_Activity]: list of activities
    """
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
    """Get summary of activity
    TODO: Change to gget graph of activity

    Args:
        db (Session): database session to run query on
        activity_name (str): actvity name to query

    Returns:
        list[Daily_Activity] | None: returns activity list queried by name or none if none found.
    """
    query = db.query(Daily_Activity)
    if activity_name:
        query = query.filter(Daily_Activity.name == activity_name.lower())
        return query.order_by(Daily_Activity).all()
    else:
        return None
