# backend/models.py
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from database import Base

class NetWorthRecord(Base):
    __tablename__ = "networth"

    id = Column(Integer, primary_key=True, index=True)
    cash = Column(Integer)
    stock = Column(Integer)
    savings = Column(Integer)
    real_estate = Column(Integer)
    loan = Column(Integer)
    credit_card = Column(Integer)
    jeonse = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)