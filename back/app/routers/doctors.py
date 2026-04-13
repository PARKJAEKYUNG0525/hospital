from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.db.scheme.doctors import DoctorCreate,DoctorResponse,DoctorUpdate
from app.services.doctors import DoctorService as service

router = APIRouter(prefix="/doctors", tags=["Doctor"])

# C 생성
@router.post("", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor(
    data: DoctorCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.create_doctor_service(db, data)

# R 전체 조회
@router.get("", response_model=list[DoctorResponse])
async def list_doctors(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_all_doctor_service(db)

# R 단일 조회
@router.get("/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_doctor_service(db, doctor_id)

# U 변경
@router.put("/{doctor_id}", response_model=DoctorResponse)
async def update_patient(
    doctor_id: int, 
    data: DoctorUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.update_doctor_service(db, doctor_id,data)

# D 삭제
@router.delete("/{doctor_id}")
async def delete_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_doctor_service(db, doctor_id)