# yisangwook/financial_web/financial_web-146fb0d6e55801ae7ac6fdd7de80954704459859/backend/routers/networth.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models # models.py 전체를 가져오도록 수정

router = APIRouter()

# 데이터베이스 세션을 가져오는 함수 (FastAPI 권장 방식)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request model (기존과 동일)
class FinancialData(BaseModel):
    cash: int
    stock: int
    savings: int
    real_estate: int
    loan: int
    credit_card: int
    jeonse: int

# Response model (기존과 동일)
class NetWorthResult(BaseModel):
    total_assets: int
    total_liabilities: int
    net_worth: int

# POST 요청: 순자산 계산 및 DB 저장
@router.post("/api/networth", response_model=NetWorthResult)
def calculate_and_save_net_worth(data: FinancialData, db: Session = Depends(get_db)):
    # 1. 순자산 계산
    total_assets = data.cash + data.stock + data.savings + data.real_estate
    total_liabilities = data.loan + data.credit_card + data.jeonse
    net_worth = total_assets - total_liabilities

    # 2. DB에 저장할 객체 생성 (올바른 모델과 필드 사용)
    db_record = models.NetWorthRecord(
        cash=data.cash,
        stock=data.stock,
        savings=data.savings,
        real_estate=data.real_estate,
        loan=data.loan,
        credit_card=data.credit_card,
        jeonse=data.jeonse,
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        net_worth=net_worth
    )

    # 3. DB에 추가, 저장(commit), 및 새로고침
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # 4. 프론트엔드에 계산 결과 반환
    return db_record


# GET 요청: 저장된 모든 순자산 기록 가져오기
@router.get("/api/networth", response_model=List[NetWorthResult])
def get_all_net_worth_records(db: Session = Depends(get_db)):
    records = db.query(models.NetWorthRecord).all()
    return records