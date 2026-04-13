from pydantic import BaseModel
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    name: str
    birth_date: date
    gender: str


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    name: str
    birth_date: date
    gender: str

    class Config:
        from_attributes = True