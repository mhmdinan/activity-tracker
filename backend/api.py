from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import (
    get_activity,
    create_activity,
    add_in_activity,
    get_daily_acitivies,
    get_activity_summary
)
import schemas
from db import get_db

api = APIRouter()

@api.get("/get-activity/{activity_name}")
def get_activity_api(
    activity_name: str,
    db: Session = Depends(get_db)
):
    activity = get_activity(db, activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="activity not found")
    return JSONResponse(
        status_code=200,
        content=activity
    )

@api.post("create-activity")
def create_activity_api(
    activity: schemas.DailyActivityCreate,
    db: Session = Depends(get_db)
):
    activity = create_activity(db, activity)
    return JSONResponse(
        status_code=200,
        content=activity
    )

@api.post("/add-in-activity")
def add_in_activity_api():
    return

@api.get("/get-daily-activites")
def get_daily_acitivies_api():
    return

@api.get("/get-activity-summary")
def get_activity_summary_api():
    return