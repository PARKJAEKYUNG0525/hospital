from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.db.database import get_db
from app.db.scheme.appointments import AppointmentCreate, AppointmentResponse,AppointmentStatusUpdate
from app.services.appointments import AppointmentService as service

router = APIRouter(prefix="/appointments", tags=["Appointment"])


# C 생성
@router.post("", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await service.create_appointment_service(db, appointment_data)


# R 전체 조회 
@router.get("", response_model=List[AppointmentResponse])
async def list_appointments(
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    if status:
        return await service.get_appointments_by_status_service(db, status)
    return await service.get_all_appointments_service(db)

# R 단일 조회
@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_appointment_by_id_service(db, appointment_id)

# U 변경 
@router.patch("/{appointment_id}/status", response_model=AppointmentResponse)
async def update_appointment_status(
    appointment_id: int,
    status_data: AppointmentStatusUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.update_appointment_status_service(db, appointment_id, status_data)

# 취소
async def cancel_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    status_data = AppointmentStatusUpdate(status="canceled")
    return await service.update_appointment_status_service(db, appointment_id, status_data)

# D 삭제
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db)
):
    await service.delete_appointment_service(db, appointment_id)
    return None