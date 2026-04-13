from sqlalchemy.future import select
from app.db.models.doctors import Doctor
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.scheme.doctors import DoctorCreate
from fastapi import HTTPException

class DoctorCrud:

     # C 생성
    @staticmethod
    async def create_doctor(db:AsyncSession, doctor: DoctorCreate):
        db_doctor = Doctor(**doctor.model_dump())
        db.add(db_doctor)
        await db.flush()
        return db_doctor

    # R 전체 조회
    @staticmethod
    async def get_all_doctor(db:AsyncSession):
        result = await db.execute(select(Doctor))
        return result.scalars().all()

    # R 단일 조회
    @staticmethod
    async def get_doctor(db:AsyncSession, doctor_id: int):
        result = await db.execute(
            select(Doctor).where(Doctor.id == doctor_id)
        )
        doctor= result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail=f"ID {doctor_id}번 의사를 찾을 수 없습니다.")
        return doctor
    
    # U 변경
    @staticmethod
    async def update_doctor(db: AsyncSession, doctors: Doctor, data):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(doctors, key, value)
        await db.flush()
        return doctors


    # D 삭제
    @staticmethod
    async def delete_doctor(db:AsyncSession, doctor_id:int):
        result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
        doctor = result.scalar_one_or_none()
        if not doctor:
            raise HTTPException(status_code=404, detail=f"ID {doctor_id}번 의사를 찾을 수 없어 삭제할 수 없습니다.")
        await db.delete(doctor)
        await db.flush()
        return doctor
    
doctors_crud = DoctorCrud()
    