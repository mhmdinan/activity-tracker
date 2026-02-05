from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from crud import (
    get_activity,
    create_activity,
    add_in_activity,
    get_activity_data,
    get_activity_plot,
    get_daily_acitivies,
)
import schemas
from db import get_db

api = APIRouter()


@api.get("/get-activity/{activity_name}", response_model=schemas.DailyActivtyView)
def get_activity_api(activity_name: str, db: Session = Depends(get_db)):
    activity = get_activity(db, activity_name)
    if activity is None:
        raise HTTPException(status_code=404, detail="activity not found")
    return activity


@api.post("/create-activity", response_model=schemas.DailyActivtyView)
def create_activity_api(
    activity: schemas.DailyActivityCreate, db: Session = Depends(get_db)
):
    activity = create_activity(db, activity)
    return activity


@api.post("/add-in-activity")
def add_in_activity_api(
    updated_activity: schemas.DailyActivityUpdate, db: Session = Depends(get_db)
):
    activity = add_in_activity(db, updated_activity)
    if activity is None:
        raise HTTPException(status_code=404, detail="activity not found")
    return activity


@api.get(
    "/get-daily-activities", response_model=List[schemas.DailyActivtyView]
)
def get_daily_acitivies_api(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return get_daily_acitivies(db, skip, limit)


@api.get("/get-activity-data/{activity_name}")
def get_activity_data_api(
    activity_name: str, day_count: int , db: Session = Depends(get_db)
):
    activity = get_activity_data(db, activity_name, day_count)
    if activity is None:
        raise HTTPException(status_code=404, detail="activity not found")
    return JSONResponse(status_code=200, content=activity)

@api.get("/get-activity-plot/{activity_name}")
def get_activity_plot_api(
    activity_name: str, day_count: int, db: Session = Depends(get_db)
):
    image_data = get_activity_plot(db, activity_name, day_count)
    if image_data is None:
        raise HTTPException(status_code=404, detail='No data for activity exists')
    return {
        "activity": activity_name,
        "image": f"data:image/png;base64,{image_data}"
    }
