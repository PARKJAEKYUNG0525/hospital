from pydantic import BaseModel
from typing import Optional

class PrescriptionCreate(BaseModel):
    appointment_id: int
    medicine_name: str


class PrescriptionUpdate(BaseModel):
    medicine_name: Optional[str] = None


class PrescriptionResponse(BaseModel):
    id: int
    appointment_id: int
    medicine_name: str

    class Config:
        from_attributes = True