import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from fastapi.concurrency import asynccontextmanager
from dotenv import load_dotenv
from app.routers import appointments,prescriptions,wards,doctors,patients
# from app.middleware.token_refresh import TokenRefreshMiddleware

load_dotenv(dotenv_path=".env")

#DB연결 후 metadata.create_all -> 모든 테이블 생성 
#종료시에 DB연결 해제 
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app=FastAPI(lifespan=lifespan)

# app.add_middleware(TokenRefreshMiddleware)


# CORSMiddleware : 다른 도메인, 포트에서 오는 요청을 허용하도록 하는 미들웨어
# allow_origins : 요청을 허용할 출처 리스트
# allow_credentials : 로그인 / jwt 기반 인증필요한 경우(쿠키, 세션정보등 요청 허용)
# allow_methods : HTTP모든 메소드 다 허용

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
app.include_router(prescriptions.router)
app.include_router(wards.router)

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081, reload=True)


