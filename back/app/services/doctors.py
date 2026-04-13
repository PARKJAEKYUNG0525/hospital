from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.doctors import DoctorCrud as crud
from app.db.scheme.doctors import DoctorCreate,DoctorUpdate


class DoctorService:
    # C 생성 
    @staticmethod
    async def create_doctor_service(db: AsyncSession, data:DoctorCreate):
        try:
            doctor = await crud.create_doctor(db, data)
            await db.commit()
            await db.refresh(doctor)
            return doctor
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"의사 생성 중 오류: {str(e)}")
    
    # R 전체 조회
    @staticmethod
    async def get_all_doctor_service(db: AsyncSession):
        try:
            return await crud.get_all_doctor(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"전체 조회 중 오류: {str(e)}")
    
    # R 단일 조회
    @staticmethod
    async def get_doctor_service(db: AsyncSession, doctor_id: int):
        try:
            return await crud.get_doctor(db, doctor_id)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"조회 중 오류: {str(e)}")
    
    # U 변경
    @staticmethod
    async def update_doctor_service(db: AsyncSession, patient_id: int, data: DoctorUpdate):
        try:
            patient = await crud.get_doctor(db, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail=f"ID {patient_id} 의사를 찾을 수 없습니다.")
            
            updated = await crud.update_doctor(db, patient, data)
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
    async def delete_doctor_service(db: AsyncSession, doctor_id: int):
        try:
            doctor = await crud.get_doctor(db, doctor_id)
            if not doctor:
                raise HTTPException(status_code=404, detail=f"ID {doctor_id} 의사를 찾을 수 없습니다.")
            await crud.delete_doctor(db, doctor_id)
            await db.commit()
            return {"message": f"ID {doctor_id}번 의사 정보가 성공적으로 삭제되었습니다."}
            
        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 서버 오류 발생: {str(e)}")