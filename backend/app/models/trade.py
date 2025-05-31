from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from app.db.base import Base

class OrderType(enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderSide(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(String, unique=True, index=True)
    trading_symbol = Column(String, index=True)
    order_type = Column(Enum(OrderType))
    side = Column(Enum(OrderSide))
    quantity = Column(Integer)
    price = Column(Float)
    status = Column(Enum(OrderStatus))
    pnl = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 