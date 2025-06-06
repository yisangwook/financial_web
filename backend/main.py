# yisangwook/financial_web/financial_web-146fb0d6e55801ae7ac6fdd7de80954704459859/backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import networth
import models
from database import engine

# models.py에 정의된 모든 테이블을 데이터베이스에 생성합니다.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 미들웨어 추가 (이 부분은 원래 코드와 동일합니다)
origins = [
    "http://localhost:3000",
    "https://financial-web-mjhg.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# networth.py에 정의된 라우터들을 앱에 포함시킵니다.
app.include_router(networth.router)