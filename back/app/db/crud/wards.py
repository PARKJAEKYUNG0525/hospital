from sqlalchemy.future import select
from sqlalchemy import delete
from app.db.models.wards import Ward
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from app.db.scheme.wards import WardCreate
from fastapi import HTTPException



class WardCrud:
    # C 생성
    @staticmethod
    async def create_ward(db:AsyncSession, ward: WardCreate):
        db_ward = Ward(**ward.model_dump())
        db.add(db_ward)
        await db.flush()
        return db_ward

    # R 전체 조회
    @staticmethod
    async def get_all_ward(db:AsyncSession):
        result = await db.execute(select(Ward))
        return result.scalars().all()

    # R 단일 조회
    @staticmethod
    async def get_ward(db:AsyncSession, ward_id: int):
        result = await db.execute(
            select(Ward).options(joinedload(Ward.doctor)).where(Ward.id == ward_id)
        )
        ward= result.scalar_one_or_none()
        if not ward:
            raise HTTPException(status_code=404, detail=f"ID {ward_id}번 병동을 찾을 수 없습니다.")
        return ward

    # U 변경
    @staticmethod
    async def update_ward(db: AsyncSession, doctors: Ward, data):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(doctors, key, value)
        await db.flush()
        return doctors
    
    # D 삭제
    @staticmethod
    async def delete_ward(db: AsyncSession, ward_id: int):
        query = delete(Ward).where(Ward.id == ward_id)
        await db.execute(query)