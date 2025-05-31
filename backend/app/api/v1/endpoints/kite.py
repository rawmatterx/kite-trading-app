from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict
from datetime import datetime, timedelta

from app.core.kite_client import KiteClient
from app.core.config import settings
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/login")
async def login(request_token: str, current_user: User = Depends(get_current_user)):
    """Login to Kite and get access token"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        access_token = kite_client.login(request_token)
        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/margins")
async def get_margins(current_user: User = Depends(get_current_user)):
    """Get account margins"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        return kite_client.get_margins()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/positions")
async def get_positions(current_user: User = Depends(get_current_user)):
    """Get current positions"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        return kite_client.get_positions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/orders")
async def place_order(order_params: Dict, current_user: User = Depends(get_current_user)):
    """Place a new order"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        order_id = kite_client.place_order(order_params)
        return {"order_id": order_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/orders")
async def get_orders(current_user: User = Depends(get_current_user)):
    """Get all orders"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        return kite_client.get_orders()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/historical-data/{instrument_token}")
async def get_historical_data(
    instrument_token: int,
    from_date: datetime,
    to_date: datetime,
    interval: str,
    current_user: User = Depends(get_current_user)
):
    """Get historical data for an instrument"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        return kite_client.get_historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/instruments")
async def get_instruments(current_user: User = Depends(get_current_user)):
    """Get all instruments"""
    try:
        kite_client = KiteClient(settings.KITE_API_KEY, settings.KITE_API_SECRET)
        return kite_client.get_instruments()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 