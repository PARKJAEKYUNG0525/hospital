from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.scheme.wards import WardCreate, WardResponse,WardUpdate
from app.services.wards import WardService as service

router = APIRouter(prefix="/wards", tags=["Ward"])

# C 생성
@router.post("", response_model=WardResponse, status_code=status.HTTP_201_CREATED)
async def create_ward(
    data: WardCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.create_ward_service(db, data)


# R 전체 조회
@router.get("", response_model=list[WardResponse])
async def list_wards(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_all_ward_service(db)


# R 단일 조회
@router.get("/{ward_id}", response_model=WardResponse)
async def get_ward(
    ward_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await service.get_ward_service(db, ward_id)

# U 변경
@router.put("/{doctor_id}", response_model=WardResponse)
async def update_patient(
    ward_id: int, 
    data: WardUpdate,  
    db: AsyncSession = Depends(get_db)
):
    return await service.update_ward_service(db, ward_id, data)


# D 삭제
@router.delete("/{ward_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ward(
    ward_id: int, 
    db: AsyncSession = Depends(get_db)
):
    await service.delete_ward_service(db, ward_id)
    return None


