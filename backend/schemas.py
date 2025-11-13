from pydantic import BaseModel

class DailyActivityBase(BaseModel):
    name: str

class DailyActivityCreate(DailyActivityBase):
    notes: str = ""

class DailyActivityUpdate(DailyActivityBase):
    addition: int
    #notes: str | None = None

class DailyActivtyView(DailyActivityCreate):
    id: int
    count: int

    class Config:
        from_attributes = True