from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.models.appointments import Appointment
from app.db.scheme.appointments import AppointmentCreate 
from fastapi import HTTPException
from app.db.models.patients import Patient
from app.db.models.doctors import Doctor



class AppointmentCrud:

    # C 생성
    @staticmethod
    async def create_appointment(db: AsyncSession, appointment: AppointmentCreate):
        result = await db.execute(
            select(Patient).filter(Patient.id == appointment.patient_id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=404, 
                detail=f"ID가 {appointment.patient_id}인 환자를 찾을 수 없습니다."
            )
        
        doctor_result = await db.execute(
            select(Doctor).filter(Doctor.id == appointment.doctor_id)
        )
        if not doctor_result.scalar_one_or_none():
            raise HTTPException(
                status_code=404, 
                detail=f"ID {appointment.doctor_id}번 의사를 찾을 수 없습니다."
            )

        db_app = Appointment(**appointment.model_dump())
        db.add(db_app)
        await db.flush()

        final_result = await db.execute(
            select(Appointment)
            .options(
                joinedload(Appointment.patient), 
                joinedload(Appointment.doctor)
            )
            .filter(Appointment.id == db_app.id)
        )
        return final_result.scalar_one()
    
    # R 전체 조회 
    @staticmethod
    async def get_all_appointments(db: AsyncSession):
        result = await db.execute(
            select(Appointment).options(
                joinedload(Appointment.patient), 
                joinedload(Appointment.doctor)  
            )
        )
        return result.scalars().all()

    # R 단일 조회
    @staticmethod
    async def get_appointment(db: AsyncSession, appointment_id: int):
        result = await db.execute(
            select(Appointment)
            .where(Appointment.id == appointment_id)
            .options(
                joinedload(Appointment.patient), 
                joinedload(Appointment.doctor)   
            )
        )
        return result.scalar_one_or_none()
    
    # R 상태 조회
    @staticmethod
    async def get_appointments_by_status(db: AsyncSession, status: str):
        result = await db.execute(
            select(Appointment)
            .where(Appointment.status == status)
            .options(
                joinedload(Appointment.patient), 
                joinedload(Appointment.doctor)  
            )
        )
        return result.scalars().all()
    
    # U 변경
    @staticmethod
    async def update_appointment_status(db: AsyncSession, appointment_id: int, new_status: str):
        result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
        db_app = result.scalar_one_or_none()
        
        if not db_app:
            raise HTTPException(
                status_code=404, 
                detail=f"ID {appointment_id}번 예약을 찾을 수 없어 상태를 변경할 수 없습니다."
            )
        
        db_app.status = new_status
        await db.flush() 
        return db_app

    
    # D 삭제
    @staticmethod
    async def delete_appointment(db: AsyncSession, appointment_id: int):
        from sqlalchemy import delete
        query = delete(Appointment).where(Appointment.id == appointment_id)
        await db.execute(query)

    # 중복 예약 체크 (같은 의사, 같은 시간)
    @staticmethod
    async def get_duplicate_appointment(
        db: AsyncSession,
        doctor_id: int,
        appointment_date
    ):
        result = await db.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_id,
                Appointment.appointment_date == appointment_date
            )
        )
        return result.scalar_one_or_none()