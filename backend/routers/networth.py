from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
from models import NetWorth

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

    db: Session = SessionLocal()
    try:
        networth_entry = NetWorth(
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            net_worth=net_worth
        )
        db.add(networth_entry)
        db.commit()
        db.refresh(networth_entry)
    finally:
        db.close()

    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "net_worth": net_worth
    }


from typing import List

@router.get("/api/networth", response_model=List[NetWorthResult])
def get_net_worth_records():
    db: Session = SessionLocal()
    try:
        records = db.query(NetWorth).all()
        return [
            NetWorthResult(
                total_assets=r.total_assets,
                total_liabilities=r.total_liabilities,
                net_worth=r.net_worth
            ) for r in records
        ]
    finally:
        db.close()

__all__ = ["router"]
