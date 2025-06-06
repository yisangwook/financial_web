from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 허용할 출처 목록
origins = [
    "http://localhost:3000",  # local dev
    "https://financial-web-mjhg.vercel.app"  # deployed Vercel frontend
]

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 수정된 부분
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 이하 코드는 그대로 ---
class FinancialData(BaseModel):
    cash: int
    stock: int
    savings: int
    real_estate: int
    loan: int
    credit_card: int
    jeonse: int

@app.post("/api/networth")
def calculate_net_worth(data: FinancialData):
    total_assets = data.cash + data.stock + data.savings + data.real_estate
    total_liabilities = data.loan + data.credit_card + data.jeonse
    net_worth = total_assets - total_liabilities

    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_worth": net_worth,
    }