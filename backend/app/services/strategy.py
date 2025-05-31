import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.models.trade import Trade, OrderType, OrderSide, OrderStatus
from app.services.kite import KiteService

logger = logging.getLogger(__name__)

class StrategyService:
    def __init__(self, db: Session, strategy: Strategy, kite_service: KiteService):
        self.db = db
        self.strategy = strategy
        self.kite = kite_service
        self.is_running = False
        self.task = None

    async def start(self):
        if self.is_running:
            return
        
        self.is_running = True
        self.task = asyncio.create_task(self._run_strategy())
        logger.info(f"Strategy {self.strategy.name} started")

    async def stop(self):
        if not self.is_running:
            return
        
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info(f"Strategy {self.strategy.name} stopped")

    async def _run_strategy(self):
        while self.is_running:
            try:
                # Get historical data for analysis
                end_date = datetime.now()
                start_date = end_date - timedelta(days=1)
                data = await self.kite.get_historical_data(
                    trading_symbol=self.strategy.parameters["symbol"],
                    from_date=start_date,
                    to_date=end_date,
                    interval="5minute"
                )
                
                # Convert to DataFrame
                df = pd.DataFrame(data)
                
                # Calculate indicators
                signals = self._calculate_signals(df)
                
                # Check for trading signals
                if signals["should_buy"]:
                    await self._place_buy_order()
                elif signals["should_sell"]:
                    await self._place_sell_order()
                
                # Wait for next iteration
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in strategy execution: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying

    def _calculate_signals(self, df: pd.DataFrame) -> Dict:
        try:
            # Calculate SMA
            short_period = self.strategy.parameters.get("sma_short_period", 50)
            long_period = self.strategy.parameters.get("sma_long_period", 200)
            
            df["sma_short"] = df["close"].rolling(window=short_period).mean()
            df["sma_long"] = df["close"].rolling(window=long_period).mean()
            
            # Calculate RSI
            delta = df["close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df["rsi"] = 100 - (100 / (1 + rs))
            
            # Generate signals
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            
            # SMA crossover
            sma_crossover = (
                prev_row["sma_short"] <= prev_row["sma_long"] and
                last_row["sma_short"] > last_row["sma_long"]
            )
            
            sma_crossunder = (
                prev_row["sma_short"] >= prev_row["sma_long"] and
                last_row["sma_short"] < last_row["sma_long"]
            )
            
            # RSI conditions
            rsi_oversold = last_row["rsi"] < 30
            rsi_overbought = last_row["rsi"] > 70
            
            return {
                "should_buy": sma_crossover and rsi_oversold,
                "should_sell": sma_crossunder and rsi_overbought
            }
            
        except Exception as e:
            logger.error(f"Error calculating signals: {str(e)}")
            return {"should_buy": False, "should_sell": False}

    async def _place_buy_order(self):
        try:
            # Get current quote
            quote = await self.kite.get_quote(self.strategy.parameters["symbol"])
            current_price = quote["last_price"]
            
            # Calculate position size
            position_size = min(
                self.strategy.max_position_size,
                self.strategy.parameters.get("position_size", 100000)
            )
            
            # Calculate quantity
            quantity = int(position_size / current_price)
            
            # Place order
            order = await self.kite.place_order(
                trading_symbol=self.strategy.parameters["symbol"],
                order_type="MARKET",
                side="BUY",
                quantity=quantity
            )
            
            # Record trade in database
            db_trade = Trade(
                user_id=self.strategy.user_id,
                order_id=order["order_id"],
                trading_symbol=self.strategy.parameters["symbol"],
                order_type=OrderType.MARKET,
                side=OrderSide.BUY,
                quantity=quantity,
                price=current_price,
                status=OrderStatus.PENDING
            )
            self.db.add(db_trade)
            self.db.commit()
            
            logger.info(f"Buy order placed: {order['order_id']}")
            
        except Exception as e:
            logger.error(f"Error placing buy order: {str(e)}")

    async def _place_sell_order(self):
        try:
            # Get current positions
            positions = await self.kite.get_positions()
            position = next(
                (p for p in positions if p["trading_symbol"] == self.strategy.parameters["symbol"]),
                None
            )
            
            if not position or position["quantity"] <= 0:
                return
            
            # Get current quote
            quote = await self.kite.get_quote(self.strategy.parameters["symbol"])
            current_price = quote["last_price"]
            
            # Place order
            order = await self.kite.place_order(
                trading_symbol=self.strategy.parameters["symbol"],
                order_type="MARKET",
                side="SELL",
                quantity=position["quantity"]
            )
            
            # Record trade in database
            db_trade = Trade(
                user_id=self.strategy.user_id,
                order_id=order["order_id"],
                trading_symbol=self.strategy.parameters["symbol"],
                order_type=OrderType.MARKET,
                side=OrderSide.SELL,
                quantity=position["quantity"],
                price=current_price,
                status=OrderStatus.PENDING
            )
            self.db.add(db_trade)
            self.db.commit()
            
            logger.info(f"Sell order placed: {order['order_id']}")
            
        except Exception as e:
            logger.error(f"Error placing sell order: {str(e)}") 