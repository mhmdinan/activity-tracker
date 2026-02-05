from pydantic import BaseModel, ConfigDict

class DailyActivityBase(BaseModel):
    name: str

class DailyActivityCreate(DailyActivityBase):
    notes: str = ""
    goal: int

class DailyActivityUpdate(DailyActivityBase):
    addition: int

class DailyActivtyView(DailyActivityCreate):
    id: int
    goal: int

    model_config = ConfigDict(from_attributes = True)

