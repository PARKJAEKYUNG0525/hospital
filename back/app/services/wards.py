from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.crud.wards import WardCrud as crud
from app.db.scheme.wards import WardCreate,WardUpdate

class WardService:
    # C 생성
    @staticmethod
    async def create_ward_service(db: AsyncSession, data:WardCreate):
        try:
            db_ward = await crud.create_ward(db, data)
            await db.commit()
            await db.refresh(db_ward)
            return db_ward
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"병동 생성 중 오류: {str(e)}")
        
    # R 전체 조회
    @staticmethod
    async def get_all_ward_service(db: AsyncSession):
        try:
            return await crud.get_all_ward(db)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"전체 조회 중 오류: {str(e)}")

    # R 단일 조회
    @staticmethod
    async def get_ward_service(db: AsyncSession,ward_id: int):        
        try:
            db_app = await crud.get_ward(db, ward_id) 
            if not db_app:
                raise HTTPException(
                    status_code=404, 
                    detail=f"ID {ward_id}번 예약을 찾을 수 없습니다."
                )
            return db_app
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"조회 중 오류: {str(e)}")

    # U 변경
    @staticmethod
    async def update_ward_service(db: AsyncSession, ward_id: int, data: WardUpdate):
        try:
            ward = await crud.get_ward(db, ward_id)
            if not ward:
                raise HTTPException(status_code=404, detail=f"ID {ward_id} 병동을 찾을 수 없습니다.")

            updated = await crud.update_ward(db, ward, data)
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
    async def delete_ward_service(db: AsyncSession, ward_id: int):
        try:
            ward = await crud.get_ward(db, ward_id)
            if not ward:
                raise HTTPException(status_code=404, detail="삭제할 병동을 찾을 수 없습니다.")
            await crud.delete_ward(db, ward_id)
            
            # 3. 트랜잭션 확정
            await db.commit()
        except HTTPException as e:
            await db.rollback()
            raise e
        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"병동 삭제 중 오류 발생: {str(e)}")