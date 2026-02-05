import base64
import io
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Daily_Activity, Daily_Log
from datetime import date
import schemas
import matplotlib.pyplot as plt


def get_activity(db: Session, name: str) -> Daily_Activity | None:
    activity = (
        db.query(Daily_Activity).filter(Daily_Activity.name == name.lower()).first()
    )
    if activity:
        return activity
    else:
        return None


def create_activity(
    db: Session, created_activity: schemas.DailyActivityCreate
) -> Daily_Activity:
    activity = (
        db.query(Daily_Activity)
        .filter(Daily_Activity.name == created_activity.name.lower())
        .first()
    )
    if activity:
        return activity
    else:
        db_activity = Daily_Activity(name=created_activity.name.lower(), goal=0)
        db.add(db_activity)
        db.commit()
        db.refresh(db_activity)
        return db_activity


def add_in_activity(
    db: Session,
    updated_activity: schemas.DailyActivityUpdate,
) -> Daily_Activity | None:
    activity = (
        db.query(Daily_Activity)
        .filter(Daily_Activity.name == updated_activity.name.lower())
        .first()
    )

    if activity:
        daily_log = (
            db.query(Daily_Log)
            .filter(
                Daily_Log.activity == Daily_Activity,
                func.date(Daily_Log.date) == date.today(),
            )
            .first()
        )
        if daily_log:
            daily_log.count = daily_log.count + updated_activity.addition
            db.commit()
            db.refresh(daily_log)
            return daily_log
        else:
            daily_log = Daily_Log(
                activity_id=activity.id,
                count=updated_activity.addition,
                date=date.today(),
            )
            db.add(daily_log)
            db.commit()
            db.refresh(daily_log)
            return daily_log
    else:
        return None


def get_daily_acitivies(
    db: Session, skip: int = 0, limit: int = 20
) -> list[Daily_Activity]:
    return db.query(Daily_Activity).offset(skip).limit(limit)


def get_activity_data(
    db: Session, activity_name: str, day_count: int
) -> list[Daily_Log]:
    activity_data = (
        db.query(Daily_Log)
        .join(Daily_Activity)
        .where(Daily_Activity.name == activity_name.lower())
        .order_by(Daily_Log.date.desc())
        .limit(day_count)
        .all()
    )
    return activity_data


def get_activity_plot(db: Session, activity_name: str, day_count: int):
    logs = get_activity_data(db, activity_name, day_count)
    if not logs:
        raise HTTPException(status_code=404, detail="No data found for this activity")
    dates = [log.date.strftime("%Y-%m-%d") for log in logs]
    counts = [log.count for log in logs]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker="o", linestyle="-", color="#4f46e5")

    plt.title(f"Activity: {activity_name} (Last {len(logs)} entries)")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.xticks(rotation = 45)
    plt.grid(True, linestyle="--", alpha=0.7)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    base64_img = base64.b64encode(buffer.read()).decode('uts-8')
    return base64_img
