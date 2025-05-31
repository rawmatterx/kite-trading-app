from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    kite_access_token = Column(String, nullable=True)
    kite_refresh_token = Column(String)
    telegram_chat_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    max_position_size = Column(Float, default=100000.0)  # ₹1L
    max_daily_loss = Column(Float, default=5000.0)  # ₹5K 