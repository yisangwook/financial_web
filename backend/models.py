# yisangwook/financial_web/financial_web-146fb0d6e55801ae7ac6fdd7de80954704459859/backend/models.py

from sqlalchemy import Column, Integer, BigInteger, DateTime
from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey, String, Boolean # String, Boolean, ForeignKey 임포트
from sqlalchemy.orm import relationship # relationship 임포트

class NetWorthRecord(Base):
    __tablename__ = "networth_records" # 테이블 이름 변경 (더 명확하게)

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # --- 입력값 ---
    cash = Column(BigInteger)
    stock = Column(BigInteger)
    savings = Column(BigInteger)
    real_estate = Column(BigInteger)
    loan = Column(BigInteger)
    credit_card = Column(BigInteger)
    jeonse = Column(BigInteger)

    # --- 계산 결과 (추가) ---
    total_assets = Column(BigInteger)
    total_liabilities = Column(BigInteger)
    net_worth = Column(BigInteger)