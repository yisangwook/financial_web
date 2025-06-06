

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 입력 데이터 모델
class FinancialData(BaseModel):
    cash: int
    stock: int
    savings: int
    real_estate: int
    loan: int
    credit_card: int
    jeonse: int

# 순자산 계산 API
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