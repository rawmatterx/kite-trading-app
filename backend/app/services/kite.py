from kiteconnect import KiteConnect
from typing import Optional, Dict, List
import logging
from datetime import datetime, timedelta

from app.core.config import settings
from app.models.user import User

logger = logging.getLogger(__name__)

class KiteService:
    def __init__(self, user: User):
        self.user = user
        self.kite = KiteConnect(api_key=settings.KITE_API_KEY)
        if user.kite_access_token:
            self.kite.set_access_token(user.kite_access_token)

    async def place_order(
        self,
        trading_symbol: str,
        order_type: str,
        side: str,
        quantity: int,
        price: Optional[float] = None
    ) -> Dict:
        try:
            order_params = {
                "tradingsymbol": trading_symbol,
                "exchange": "NSE",
                "transaction_type": side,
                "quantity": quantity,
                "product": "CNC",
                "order_type": order_type,
            }
            
            if order_type == "LIMIT" and price:
                order_params["price"] = price

            order_id = self.kite.place_order(**order_params)
            return {"order_id": order_id}
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            raise

    async def cancel_order(self, order_id: str) -> Dict:
        try:
            self.kite.cancel_order(order_id=order_id)
            return {"message": "Order cancelled successfully"}
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise

    async def get_order_status(self, order_id: str) -> Dict:
        try:
            order = self.kite.order_history(order_id)[-1]
            return {
                "order_id": order["order_id"],
                "status": order["status"],
                "trading_symbol": order["tradingsymbol"],
                "transaction_type": order["transaction_type"],
                "quantity": order["quantity"],
                "price": order["price"],
                "average_price": order["average_price"],
                "filled_quantity": order["filled_quantity"],
                "pending_quantity": order["pending_quantity"],
                "order_timestamp": order["order_timestamp"],
                "exchange_timestamp": order["exchange_timestamp"],
            }
        except Exception as e:
            logger.error(f"Error getting order status: {str(e)}")
            raise

    async def get_positions(self) -> List[Dict]:
        try:
            positions = self.kite.positions()
            return [
                {
                    "trading_symbol": pos["tradingsymbol"],
                    "quantity": pos["quantity"],
                    "average_price": pos["average_price"],
                    "last_price": pos["last_price"],
                    "pnl": pos["pnl"],
                    "product": pos["product"],
                }
                for pos in positions["net"]
                if pos["quantity"] != 0
            ]
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            raise

    async def get_historical_data(
        self,
        trading_symbol: str,
        from_date: datetime,
        to_date: datetime,
        interval: str = "5minute"
    ) -> List[Dict]:
        try:
            data = self.kite.historical_data(
                instrument_token=self._get_instrument_token(trading_symbol),
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
            return data
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            raise

    def _get_instrument_token(self, trading_symbol: str) -> int:
        try:
            instruments = self.kite.instruments("NSE")
            instrument = next(
                (i for i in instruments if i["tradingsymbol"] == trading_symbol),
                None
            )
            if not instrument:
                raise ValueError(f"Instrument {trading_symbol} not found")
            return instrument["instrument_token"]
        except Exception as e:
            logger.error(f"Error getting instrument token: {str(e)}")
            raise

    async def get_quote(self, trading_symbol: str) -> Dict:
        try:
            quote = self.kite.quote(f"NSE:{trading_symbol}")
            return {
                "trading_symbol": trading_symbol,
                "last_price": quote["last_price"],
                "ohlc": quote["ohlc"],
                "volume": quote["volume"],
                "change": quote["change"],
            }
        except Exception as e:
            logger.error(f"Error getting quote: {str(e)}")
            raise 