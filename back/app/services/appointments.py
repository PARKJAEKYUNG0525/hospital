from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.db.crud.appointments import AppointmentCrud as crud
from app.db.scheme.appointments import AppointmentCreate, AppointmentStatusUpdate
from datetime import datetime

class AppointmentService:
    # C 생성
    @staticmethod
    async def create_appointment_service(db: AsyncSession, data: AppointmentCreate):
        try:
            if data.appointment_date < datetime.now():
                raise HTTPException(
                    status_code=400, 
                    detail="과거 날짜로는 예약할 수 없습니다. 현재 시간 이후를 선택해주세요."
                )
            # 중복 예약 체크 (같은 의사, 같은 시간)
            existing = await crud.get_duplicate_appointment(
                db, 
                data.doctor_id, 
                data.appointment_date
            )
            if existing:
                raise HTTPException(status_code=400, detail="해당 시간에 이미 의사의 예약이 있습니다.")
            
            appointment = await crud.create_appointment(db, data)
            await db.commit()
            await db.refresh(appointment, ["patient", "doctor"])
            return appointment
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

    # R 전체 조회
    @staticmethod
    async def get_all_appointments_service(db: AsyncSession):
        try:
            return await crud.get_all_appointments(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"전체 조회 중 서버 오류: {str(e)}")

    # R 단일 조회
    @staticmethod
    async def get_appointment_by_id_service(db: AsyncSession, appointment_id: int):
        try:
            appointment = await crud.get_appointment(db, appointment_id) 
            if not appointment:
                raise HTTPException(status_code=404, detail=f"ID {appointment_id}번 예약을 찾을 수 없습니다.")
            return appointment
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"상세 조회 중 오류: {str(e)}")


    # R 상태 조회
    @staticmethod
    async def get_appointments_by_status_service(db: AsyncSession, status: str):
        try:
            return await crud.get_appointments_by_status(db, status)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"필터 조회 중 오류: {str(e)}")
        
    # U 변경
    @staticmethod
    async def update_appointment_status_service(db: AsyncSession, appointment_id: int, status_data: AppointmentStatusUpdate):
        try:
            appointment = await crud.get_appointment(db, appointment_id)
            if not appointment:
                raise HTTPException(status_code=404, detail=f"ID {appointment_id} 예약을 찾을 수 없습니다.")            

            updated = await crud.update_appointment_status(db, appointment_id, status_data.status )
            await db.commit()
            await db.refresh(updated)
            return updated
        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

    # D 삭제
    @staticmethod
    async def delete_appointment_service(db: AsyncSession, appointment_id: int):
        try:
            appointment = await crud.get_appointment(db, appointment_id)
            if not appointment:
                raise HTTPException(
                    status_code=404, 
                    detail=f"ID {appointment_id}번 예약을 찾을 수 없어 삭제가 불가능합니다."
                )
            await crud.delete_appointment(db, appointment_id)
            await db.commit()
            return {"message": f"ID {appointment_id}번 예약이 성공적으로 삭제되었습니다."}

        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 서버 오류 발생: {str(e)}")
        