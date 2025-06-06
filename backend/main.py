from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.networth import router as networth_router
from database import init_db

app = FastAPI()

init_db()

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

app.include_router(networth_router)