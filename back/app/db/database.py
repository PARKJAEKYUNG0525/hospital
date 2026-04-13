from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# 1. 주소 변경: mysql+pymysql 대신 mysql+aiomysql 사용
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:1234@localhost:3306/hospital"

# 2. 비동기 엔진 생성 (create_engine -> create_async_engine)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 3. 비동기 세션 메이커 설정 (async_sessionmaker 사용)
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# 4. get_db 함수 수정
async def get_db():
    async with SessionLocal() as db: # 이제 여기서 에러가 나지 않습니다.
        try:
            yield db
        finally:
            await db.close() # 비동기이므로 close도 await 필수!