from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models.prescriptions import Prescription
from app.db.models.appointments import Appointment
from app.db.scheme.prescriptions import PrescriptionCreate, PrescriptionUpdate


class prescriptionCrud:
    
    # C 생성
    @staticmethod
    async def create_prescription(db: AsyncSession, data : PrescriptionCreate):
        result = await db.execute(
            select(Appointment).where(Appointment.id == data.appointment_id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=404, 
                detail=f"ID {data.appointment_id}번 예약이 존재하지 않습니다."
            )
        
        db_prescription = Prescription(**data.dict())
        db.add(db_prescription)
        await db.flush()
        return db_prescription
    
    # R 전체 조회 
    @staticmethod
    async def get_all_prescriptions(db: AsyncSession):
        result = await db.execute(select(Prescription))
        return result.scalars().all()
    
    # R 단일 조회
    @staticmethod
    async def get_prescription(db: AsyncSession, prescription_id: int):
        result = await db.execute(
            select(Prescription).where(Prescription.id == prescription_id)
        )
        prescription = result.scalar_one_or_none()
        if not prescription:
            raise HTTPException(status_code=404, detail=f"ID {prescription_id}번 처방을 찾을 수 없습니다.")
        return prescription

    # R 상태 조회 
    @staticmethod
    async def get_by_appointment(db: AsyncSession, appointment_id: int):
        result = await db.execute(
            select(Prescription).where(Prescription.appointment_id == appointment_id)
        )
        return result.scalars().all()

    # U 변경
    @staticmethod
    async def update_prescription(db: AsyncSession, prescription: Prescription, data : PrescriptionUpdate):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(prescription, key, value)
        await db.flush()
        return prescription

    # D 삭제
    @staticmethod
    async def delete_prescription(db: AsyncSession, prescription: Prescription):
        await db.delete(prescription)
        await db.flush()
        return prescription