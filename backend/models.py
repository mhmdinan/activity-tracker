from datetime import datetime
from db import base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List

class Daily_Activity(base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    goal: Mapped[int] = mapped_column(nullable=False)
    logs: Mapped[List["Daily_Log"]] = relationship(back_populates="activity")

class Daily_Log(base):
    __tablename__ = "daily_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activity.id"))
    count: Mapped[int] = mapped_column(default=0)
    date: Mapped[datetime] = mapped_column(default=datetime.today)
    activity: Mapped["Daily_Activity"] = relationship(back_populates="logs")

