from typing import Optional
from enum import Enum

from sqlmodel import SQLModel, Field


class HolidayType(str, Enum):
    normal = "normal"
    church = "church"
    country_specific = "country_specific"


class Holiday(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: Optional[HolidayType] = Field(sa_column=HolidayType)
    day: int = Field(index=True)
    month: int = Field(index=True)
