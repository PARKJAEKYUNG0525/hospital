from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models.patients import Patient
from app.db.scheme.patients import PatientCreate, PatientUpdate

class PatientCrud:

    # C 생성
    @staticmethod
    async def create_patient(db: AsyncSession, data : PatientCreate):
        db_patient = Patient(**data.dict())
        db.add(db_patient)
        await db.flush()
        return db_patient
    
    # R 전체 조회
    @staticmethod
    async def get_all_patients(db: AsyncSession):
        result = await db.execute(select(Patient))
        return result.scalars().all()
    
    # R 단일 조회
    @staticmethod
    async def get_patient(db: AsyncSession, patient_id: int):
        result = await db.execute(
            select(Patient).where(Patient.id == patient_id)
        )
        patient = result.scalar_one_or_none()
        if not patient:
            raise HTTPException(status_code=404, detail=f"ID {patient_id}번 환자를 찾을 수 없습니다.")
        return patient
    
    # U 변경
    @staticmethod
    async def update_patient(db: AsyncSession, patient: Patient, data):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(patient, key, value)
        await db.flush()
        return patient
    
    # D 삭제
    @staticmethod
    async def delete_patient(db:AsyncSession, patient_id:int):
        result = await db.execute(select(Patient).where(Patient.id == patient_id))
        patient = result.scalar_one_or_none()
        if not patient:
            raise HTTPException(status_code=404, detail=f"ID {patient_id}번 환자를 찾을 수 없어 삭제할 수 없습니다.")
        await db.delete(patient)
        await db.flush()
        return patient
