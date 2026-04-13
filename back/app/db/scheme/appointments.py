from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import field_validator

# 환자 정보 요약 (이름 등을 보여주기 위해)
class PatientSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# 의사 정보 요약 (이름 등을 보여주기 위해)
class DoctorSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# 예약 생성 
class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str = "SCHEDULED"

    @field_validator("appointment_date", mode="before")
    @classmethod
    def make_naive(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return v.replace(tzinfo=None) if v.tzinfo else v

# 예약 응답 (joinedload 결과를 담기 위해 patient, doctor 추가)
class AppointmentResponse(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    status: str
    
    # 이 부분이 추가되어야 이름(Name)이 나옵니다!
    patient: Optional[PatientSimple] = None 
    doctor: Optional[DoctorSimple] = None

    class Config:
        from_attributes = True

# 상태 업데이트 (PATCH 요청용)
class AppointmentStatusUpdate(BaseModel):
    status: str