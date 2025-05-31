from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from app.db.session import get_db
from app.models.strategy import Strategy
from app.models.user import User
from app.api.v1.auth import get_current_user
from app.services.kite import KiteService
from app.services.strategy_manager import StrategyManager

router = APIRouter()
strategy_manager = StrategyManager(None)  # Will be initialized with DB session

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None
    parameters: dict
    max_position_size: float
    max_daily_loss: float

class StrategyCreate(StrategyBase):
    pass

class StrategyResponse(StrategyBase):
    id: int
    user_id: int
    is_active: bool

    class Config:
        from_attributes = True

@router.post("/", response_model=StrategyResponse)
async def create_strategy(
    strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_strategy = Strategy(
        user_id=current_user.id,
        name=strategy.name,
        description=strategy.description,
        parameters=strategy.parameters,
        max_position_size=strategy.max_position_size,
        max_daily_loss=strategy.max_daily_loss
    )
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.get("/", response_model=List[StrategyResponse])
async def get_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategies = db.query(Strategy).filter(Strategy.user_id == current_user.id).all()
    return strategies

@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    return strategy

@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(
    strategy_id: int,
    strategy: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    if not db_strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    for key, value in strategy.dict().items():
        setattr(db_strategy, key, value)
    
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.delete("/{strategy_id}")
async def delete_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Stop strategy if it's running
    if strategy_manager.is_strategy_running(strategy_id):
        await strategy_manager.stop_strategy(strategy_id)
    
    db.delete(strategy)
    db.commit()
    return {"message": "Strategy deleted successfully"}

@router.post("/{strategy_id}/toggle")
async def toggle_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    strategy = db.query(Strategy).filter(
        Strategy.id == strategy_id,
        Strategy.user_id == current_user.id
    ).first()
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Initialize strategy manager with DB session
    strategy_manager.db = db
    
    if strategy_manager.is_strategy_running(strategy_id):
        await strategy_manager.stop_strategy(strategy_id)
        strategy.is_active = False
    else:
        kite_service = KiteService(current_user)
        await strategy_manager.start_strategy(strategy, kite_service)
        strategy.is_active = True
    
    db.commit()
    return {"message": f"Strategy {'activated' if strategy.is_active else 'deactivated'} successfully"} 