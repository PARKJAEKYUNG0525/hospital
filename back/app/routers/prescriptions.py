from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.db.scheme.prescriptions import PrescriptionCreate, PrescriptionUpdate, PrescriptionResponse
from app.services.prescriptions import prescriptionsService as service

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


# C 생성
@router.post("/", response_model=PrescriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_prescription(
    data: PrescriptionCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.create_prescription_service(db, data)

# R 전체 조회
@router.get("/", response_model=List[PrescriptionResponse])
async def get_all_prescriptions(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_all_prescriptions_service(db)

# R 단일 조회
@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(
    prescription_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_prescription_service(db, prescription_id)

# R 진료 기준 조회
@router.get("/appointment/{appointment_id}", response_model=List[PrescriptionResponse])
async def get_prescriptions_by_appointment(
    appointment_id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await service.get_by_appointment_service(db, appointment_id)

# U 변경
@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    prescription_id: int, data: PrescriptionUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.update_prescription_service(db, prescription_id, data)

# D 삭제
@router.delete("/{prescription_id}")
async def delete_prescription(
    prescription_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_prescription_service(db, prescription_id)