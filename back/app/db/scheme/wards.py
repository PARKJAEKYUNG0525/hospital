from pydantic import BaseModel
from typing import Optional

class WardCreate(BaseModel):
    ward_name: str
    room_no: int
    bed_count: int
    doctor_id: int

class WardUpdate(BaseModel):
    ward_name: Optional[str] = None
    room_no: Optional[int] = None
    bed_count: Optional[int] = None
    doctor_id: Optional[int] = None

class WardResponse(WardCreate):
    id: int
    class Config:
        from_attributes = True