from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.patients import PatientCrud as crud
from app.db.scheme.patients import PatientCreate, PatientUpdate


class PatientsService:
    
    # C 생성 
    @staticmethod
    async def create_patient_service(db: AsyncSession, data: PatientCreate):
        try:
            patient = await crud.create_patient(db, data)
            await db.commit()
            await db.refresh(patient)
            return patient
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"환자 생성 중 오류: {str(e)}")
   
    # R 전체 조회
    @staticmethod
    async def get_all_patients_service(db: AsyncSession):
        try:
            return await crud.get_all_patients(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"전체 조회 중 오류: {str(e)}")
    
    # R 단일 조회
    @staticmethod
    async def get_patient_service(db: AsyncSession, patient_id: int):
        try:
            patient = await crud.get_patient(db, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail=f"ID {patient_id} 환자를 찾을 수 없습니다.")
            return patient
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"조회 중 오류: {str(e)}")
    
    # U 변경
    @staticmethod
    async def update_patient_service(db: AsyncSession, patient_id: int, data: PatientUpdate):
        try:
            patient = await crud.get_patient(db, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail=f"ID {patient_id} 환자를 찾을 수 없습니다.")
            
            updated = await crud.update_patient(db, patient, data)
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
    async def delete_patient_service(db: AsyncSession, patient_id: int):
        try:
            patient = await crud.get_patient(db, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail=f"ID {patient_id}번 환자를 찾을 수 없어 삭제가 불가능합니다.")
            await crud.delete_patient(db, patient_id)
            await db.commit()
            return {"message": f"ID {patient_id}번 환자 정보가 성공적으로 삭제되었습니다."}

        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"삭제 중 서버 오류 발생: {str(e)}")