from pydantic import BaseModel
from typing import Optional

class DoctorCreate(BaseModel):
    name: str
    specialty: str
    license_no: str


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    license_no: Optional[str] = None

class DoctorResponse(DoctorCreate):
    id: int

    class Config:
        from_attributes = True