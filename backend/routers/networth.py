# routers/networth.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# Health check route
@router.get("/test")
def test():
    return {"message": "It works!"}

# Request model
class FinancialData(BaseModel):
    cash: int
    stock: int
    savings: int
    real_estate: int
    loan: int
    credit_card: int
    jeonse: int

# Response model
class NetWorthResult(BaseModel):
    total_assets: int
    total_liabilities: int
    net_worth: int

# Net worth calculation route
@router.post("/api/networth", response_model=NetWorthResult)
def calculate_net_worth(data: FinancialData):
    total_assets = data.cash + data.stock + data.savings + data.real_estate
    total_liabilities = data.loan + data.credit_card + data.jeonse
    net_worth = total_assets - total_liabilities
    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_worth": net_worth
    }

__all__ = ["router"]
