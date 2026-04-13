from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.prescriptions import prescriptionCrud as crud
from app.db.crud.appointments import AppointmentCrud
from app.db.scheme.prescriptions import PrescriptionCreate,PrescriptionUpdate

class prescriptionsService:

# C 생성
    @staticmethod
    async def create_prescription_service(
        db: AsyncSession,
        data: PrescriptionCreate
    ):
        try:
            appointment = await AppointmentCrud.get_appointment(db, data.appointment_id)
            if not appointment:
                raise HTTPException(status_code=404, detail="진료 정보가 존재하지 않습니다.")
            
            prescription = await crud.create_prescription(db, data)
            await db.commit()
            await db.refresh(prescription)
            return prescription

        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"처방 생성 중 오류: {str(e)}")
        
    # R 전체 조회
    @staticmethod
    async def get_all_prescriptions_service(db: AsyncSession):
        try:
            return await crud.get_all_prescriptions(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"전체 조회 중 오류: {str(e)}")
        
    # R 단일 조회
    @staticmethod
    async def get_prescription_service(db: AsyncSession, prescription_id: int):
        try:
            prescription = await crud.get_prescription(db, prescription_id)
            if not prescription:
                raise HTTPException(status_code=404, detail=f"ID {prescription_id} 처방전이 존재하지 않습니다.")
            return prescription
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"조회 중 오류: {str(e)}")
        
    # R 진료 조회
    @staticmethod
    async def get_by_appointment_service(db: AsyncSession, appointment_id: int):
        try:
            return await crud.get_by_appointment(db, appointment_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"진료별 조회 중 오류: {str(e)}")
        
    # U 변경
    @staticmethod
    async def update_prescription_service(
        db: AsyncSession,
        prescription_id: int,
        data: PrescriptionUpdate
    ):
        try:
            prescription = await crud.get_prescription(db, prescription_id)
            if not prescription:
                raise HTTPException(status_code=404, detail=f"ID {prescription_id} 처방전이 존재하지 않습니다.")
            
            updated = await crud.update_prescription(db, prescription, data)
            await db.commit()
            await db.refresh(updated)
            return updated

        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"수정 중 오류: {str(e)}")
        
    # D 삭제
    @staticmethod
    async def delete_prescription_service(db: AsyncSession, prescription_id: int):
        try:
            prescription = await crud.get_prescription(db, prescription_id)
            if not prescription:
                raise HTTPException(status_code=404, detail=f"ID {prescription_id} 처방전이 존재하지 않습니다.")
            
            await crud.delete_prescription(db, prescription)
            await db.commit()
            return {"message": "처방전 삭제됨"}

        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 오류: {str(e)}")