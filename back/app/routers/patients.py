from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.db.scheme.patients import PatientCreate, PatientUpdate, PatientResponse
from app.services.patients import PatientsService as service

router = APIRouter(prefix="/patients", tags=["Patients"])


# C 생성
@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_patient(
    data: PatientCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.create_patient_service(db, data)

# R 전체 조회
@router.get("/", response_model=List[PatientResponse])
async def get_all_patients(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_all_patients_service(db)

# R 단일 조회
@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(
    patient_id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await service.get_patient_service(db, patient_id)

# U 변경
@router.put("/{patient_id}", response_model=PatientResponse)
async def update_patient(
    patient_id: int, 
    data: PatientUpdate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.update_patient_service(db, patient_id, data)

# D 삭제
@router.delete("/{patient_id}")
async def delete_patient(
    patient_id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_patient_service(db, patient_id)