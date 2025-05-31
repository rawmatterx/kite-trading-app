from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.db.session import get_db
from app.models.trade import Trade, OrderType, OrderSide, OrderStatus
from app.models.user import User
from app.api.v1.auth import get_current_user
from app.services.kite import KiteService

router = APIRouter()

class OrderBase(BaseModel):
    trading_symbol: str
    order_type: OrderType
    side: OrderSide
    quantity: int
    price: float

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_id: str
    status: OrderStatus
    pnl: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Initialize Kite service
    kite_service = KiteService(current_user)
    
    try:
        # Place order with Kite
        kite_order = await kite_service.place_order(
            trading_symbol=order.trading_symbol,
            order_type=order.order_type.value,
            side=order.side.value,
            quantity=order.quantity,
            price=order.price if order.order_type == OrderType.LIMIT else None
        )
        
        # Record order in database
        db_order = Trade(
            user_id=current_user.id,
            order_id=kite_order["order_id"],
            trading_symbol=order.trading_symbol,
            order_type=order.order_type,
            side=order.side,
            quantity=order.quantity,
            price=order.price,
            status=OrderStatus.PENDING
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Trade).filter(Trade.user_id == current_user.id).all()
    return orders

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Trade).filter(
        Trade.id == order_id,
        Trade.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Trade).filter(
        Trade.id == order_id,
        Trade.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    if order.status not in [OrderStatus.PENDING]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel pending orders"
        )
    
    try:
        # Initialize Kite service
        kite_service = KiteService(current_user)
        
        # Cancel order with Kite
        await kite_service.cancel_order(order.order_id)
        
        # Update order status in database
        order.status = OrderStatus.CANCELLED
        db.commit()
        return {"message": "Order cancelled successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 