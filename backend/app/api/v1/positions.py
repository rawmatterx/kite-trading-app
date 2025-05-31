from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.models.trade import Trade, OrderSide
from app.models.user import User
from app.api.v1.auth import get_current_user

router = APIRouter()

class Position(BaseModel):
    trading_symbol: str
    quantity: int
    average_price: float
    last_price: float
    pnl: float
    pnl_percentage: float

    class Config:
        from_attributes = True

@router.get("/", response_model=List[Position])
async def get_positions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get all completed trades for the user
    trades = db.query(Trade).filter(
        Trade.user_id == current_user.id,
        Trade.status == "COMPLETE"
    ).all()
    
    # Calculate positions
    positions = {}
    for trade in trades:
        if trade.trading_symbol not in positions:
            positions[trade.trading_symbol] = {
                "trading_symbol": trade.trading_symbol,
                "quantity": 0,
                "average_price": 0,
                "last_price": trade.price,  # TODO: Get real-time price from Kite
                "pnl": 0,
                "pnl_percentage": 0
            }
        
        position = positions[trade.trading_symbol]
        if trade.side == OrderSide.BUY:
            new_quantity = position["quantity"] + trade.quantity
            new_value = (position["quantity"] * position["average_price"]) + (trade.quantity * trade.price)
            position["average_price"] = new_value / new_quantity if new_quantity > 0 else 0
            position["quantity"] = new_quantity
        else:
            position["quantity"] -= trade.quantity
        
        # Calculate P&L
        position["pnl"] = (position["last_price"] - position["average_price"]) * position["quantity"]
        position["pnl_percentage"] = ((position["last_price"] - position["average_price"]) / position["average_price"]) * 100 if position["average_price"] > 0 else 0
    
    # Filter out positions with zero quantity
    return [pos for pos in positions.values() if pos["quantity"] != 0]

@router.get("/{symbol}", response_model=Position)
async def get_position(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    positions = await get_positions(db, current_user)
    position = next((pos for pos in positions if pos["trading_symbol"] == symbol), None)
    
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Position not found"
        )
    
    return position 