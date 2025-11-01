from pydantic import BaseModel

class DailyActivityBase(BaseModel):
    name: str

class DailyActivityCreate(BaseModel):
    name: str
    notes: str = ""

class DailyActivtyView(DailyActivityCreate):
    id: int
    count: int

    class Config:
        orm_mode = True