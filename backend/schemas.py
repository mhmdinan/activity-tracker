from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes = True)