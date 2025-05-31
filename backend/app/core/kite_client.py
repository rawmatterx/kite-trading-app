import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable, Coroutine

from kiteconnect import KiteConnect, KiteTicker
from kiteconnect.exceptions import (
    KiteException,
    TokenException,
    NetworkException,
    InputException,
    DataException,
    OrderException,
    PermissionError
)

logger = logging.getLogger(__name__)

class KiteClient:
    """
    An enhanced Kite Connect client with rate limiting, error handling, and WebSocket support.
    """
    
    def __init__(self, api_key: str, api_secret: str):
        """
        Initialize the KiteClient.
        
        Args:
            api_key (str): Kite Connect API key
            api_secret (str): Kite Connect API secret
        """
        self.kite = KiteConnect(api_key=api_key)
        self.api_secret = api_secret
        self._access_token = None
        self._last_api_call = None
        self._rate_limit_delay = 1.0  # 1 second delay between API calls
        self._ws = None
        self._ws_connected = False
        self._ws_callbacks = {}
        self._ws_subscribed_tokens = set()
    
    async def _check_rate_limit(self):
        """Ensure we don't exceed API rate limits"""
        if self._last_api_call:
            elapsed = (datetime.now() - self._last_api_call).total_seconds()
            if elapsed < self._rate_limit_delay:
                await asyncio.sleep(self._rate_limit_delay - elapsed)
        self._last_api_call = datetime.now()
    
    def _handle_kite_exception(self, e: KiteException, context: str = ""):
        """Handle Kite API exceptions with appropriate logging"""
        error_type = e.__class__.__name__
        error_msg = str(e)
        
        if isinstance(e, TokenException):
            logger.error(f"Token error {context}: {error_msg}")
        elif isinstance(e, NetworkException):
            logger.error(f"Network error {context}: {error_msg}")
        elif isinstance(e, InputException):
            logger.error(f"Input error {context}: {error_msg}")
        elif isinstance(e, DataException):
            logger.error(f"Data error {context}: {error_msg}")
        elif isinstance(e, OrderException):
            logger.error(f"Order error {context}: {error_msg}")
        else:
            logger.error(f"Kite error {context}: {error_type} - {error_msg}")
        
        raise e
    
    # ========== Authentication ==========
    
    async def login(self, request_token: str) -> str:
        """
        Login to Kite and get access token
        
        Args:
            request_token (str): Request token from Kite Connect login flow
            
        Returns:
            str: Access token
            
        Raises:
            KiteException: If login fails
        """
        try:
            await self._check_rate_limit()
            data = self.kite.generate_session(request_token, api_secret=self.api_secret)
            self._access_token = data["access_token"]
            self.kite.set_access_token(self._access_token)
            return self._access_token
        except KiteException as e:
            self._handle_kite_exception(e, "during login")
    
    def set_access_token(self, access_token: str) -> None:
        """
        Set the access token for authenticated requests
        
        Args:
            access_token (str): Access token from Kite Connect
        """
        self._access_token = access_token
        self.kite.set_access_token(access_token)
    
    # ========== Account and User Details ==========
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get user profile details"""
        try:
            await self._check_rate_limit()
            return self.kite.profile()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching profile")
    
    async def get_margins(self) -> Dict[str, Any]:
        """
        Get account margins
        
        Returns:
            Dict containing equity and commodity margins
        """
        try:
            await self._check_rate_limit()
            return self.kite.margins()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching margins")
    
    # ========== Order Management ==========
    
    async def place_order(self, **kwargs) -> str:
        """
        Place a new order
        
        Args:
            **kwargs: Order parameters (variety, exchange, tradingsymbol, etc.)
            
        Returns:
            str: Order ID
        """
        try:
            await self._check_rate_limit()
            return self.kite.place_order(**kwargs)
        except KiteException as e:
            self._handle_kite_exception(e, f"placing order with params: {kwargs}")
    
    async def modify_order(self, **kwargs) -> str:
        """Modify an existing order"""
        try:
            await self._check_rate_limit()
            return self.kite.modify_order(**kwargs)
        except KiteException as e:
            self._handle_kite_exception(e, f"modifying order with params: {kwargs}")
    
    async def cancel_order(self, order_id: str, variety: str = None) -> str:
        """Cancel an order"""
        try:
            await self._check_rate_limit()
            return self.kite.cancel_order(order_id=order_id, variety=variety)
        except KiteException as e:
            self._handle_kite_exception(e, f"canceling order {order_id}")
    
    async def get_orders(self) -> List[Dict]:
        """Get all orders"""
        try:
            await self._check_rate_limit()
            return self.kite.orders()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching orders")
    
    # ========== Positions and Holdings ==========
    
    async def get_positions(self) -> Dict[str, Any]:
        """
        Get current positions
        
        Returns:
            Dict containing net and day positions
        """
        try:
            await self._check_rate_limit()
            return self.kite.positions()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching positions")
    
    async def get_holdings(self) -> List[Dict]:
        """Get current holdings"""
        try:
            await self._check_rate_limit()
            return self.kite.holdings()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching holdings")
    
    # ========== Market Data ==========
    
    async def get_quote(self, instruments: List[str]) -> Dict[str, Any]:
        """
        Get quote for given instruments
        
        Args:
            instruments: List of instruments in the format 'exchange:tradingsymbol' or 'exchange:tradingsymbol:instrument_token'
        """
        try:
            await self._check_rate_limit()
            return self.kite.quote(instruments)
        except KiteException as e:
            self._handle_kite_exception(e, f"fetching quotes for {instruments}")
    
    async def get_ohlc(self, instruments: List[str]) -> Dict[str, Any]:
        """Get OHLC data for given instruments"""
        try:
            await self._check_rate_limit()
            return self.kite.ohlc(instruments)
        except KiteException as e:
            self._handle_kite_exception(e, f"fetching OHLC for {instruments}")
    
    # ========== WebSocket Methods ==========
    
    def _on_ticks(self, ws, ticks):
        """Handle incoming ticks"""
        for tick in ticks:
            token = tick.get('instrument_token')
            if token in self._ws_callbacks:
                for callback in self._ws_callbacks[token]:
                    try:
                        callback(tick)
                    except Exception as e:
                        logger.error(f"Error in WebSocket callback: {e}")
    
    def _on_connect(self, ws, response):
        """Handle WebSocket connection"""
        self._ws_connected = True
        logger.info("WebSocket connected")
        # Resubscribe to previously subscribed tokens
        if self._ws_subscribed_tokens:
            tokens = list(self._ws_subscribed_tokens)
            self._ws_subscribe(tokens)
    
    def _on_close(self, ws, code, reason):
        """Handle WebSocket disconnection"""
        self._ws_connected = False
        logger.warning(f"WebSocket closed: {code} - {reason}")
    
    def _ws_subscribe(self, tokens: List[int]) -> bool:
        """Subscribe to tokens via WebSocket"""
        if not self._ws_connected:
            return False
        
        tokens = [t for t in tokens if t not in self._ws_subscribed_tokens]
        if not tokens:
            return True
            
        try:
            self._ws.subscribe(tokens)
            self._ws.set_mode(self._ws.MODE_QUOTE, tokens)
            self._ws_subscribed_tokens.update(tokens)
            return True
        except Exception as e:
            logger.error(f"Error subscribing to tokens: {e}")
            return False
    
    async def connect_websocket(self, api_key: str = None, access_token: str = None):
        """
        Initialize WebSocket connection
        
        Args:
            api_key: Kite Connect API key (optional if already set)
            access_token: Access token (optional if already logged in)
        """
        if self._ws_connected and self._ws:
            logger.warning("WebSocket already connected")
            return
        
        if not api_key:
            api_key = self.kite.api_key
        if not access_token and self._access_token:
            access_token = self._access_token
        
        if not api_key or not access_token:
            raise ValueError("API key and access token are required for WebSocket connection")
        
        # Initialize WebSocket
        self._ws = KiteTicker(api_key, access_token)
        
        # Assign callbacks
        self._ws.on_ticks = self._on_ticks
        self._ws.on_connect = self._on_connect
        self._ws.on_close = self._on_close
        
        # Connect to WebSocket in a separate thread
        self._ws.connect(threaded=True)
        
        # Wait for connection to establish
        max_retries = 10
        retry_delay = 0.5  # seconds
        
        for _ in range(max_retries):
            if self._ws_connected:
                break
            await asyncio.sleep(retry_delay)
        else:
            raise TimeoutError("Failed to establish WebSocket connection")
    
    async def disconnect_websocket(self):
        """Close WebSocket connection"""
        if self._ws:
            self._ws.close()
            self._ws_connected = False
            self._ws = None
    
    def subscribe(self, tokens: List[int], callback: Callable[[Dict], None]) -> bool:
        """
        Subscribe to real-time updates for given tokens
        
        Args:
            tokens: List of instrument tokens to subscribe to
            callback: Function to call when data is received for the token
            
        Returns:
            bool: True if subscription was successful
        """
        if not self._ws_connected:
            logger.error("WebSocket not connected")
            return False
        
        # Add callback for each token
        for token in tokens:
            if token not in self._ws_callbacks:
                self._ws_callbacks[token] = []
            if callback not in self._ws_callbacks[token]:
                self._ws_callbacks[token].append(callback)
        
        # Subscribe to tokens
        return self._ws_subscribe(tokens)
    
    def unsubscribe(self, tokens: List[int] = None, callback: Callable[[Dict], None] = None):
        """
        Unsubscribe from token updates
        
        Args:
            tokens: List of instrument tokens to unsubscribe from. If None, all tokens are unsubscribed.
            callback: Specific callback to remove. If None, all callbacks for the tokens are removed.
        """
        if not tokens:
            tokens = list(self._ws_callbacks.keys())
        
        for token in tokens:
            if token in self._ws_callbacks:
                if callback:
                    if callback in self._ws_callbacks[token]:
                        self._ws_callbacks[token].remove(callback)
                        if not self._ws_callbacks[token]:
                            del self._ws_callbacks[token]
                else:
                    del self._ws_callbacks[token]
    
    # ========== GTT (Good Till Triggered) Orders ==========
    
    async def place_gtt(self, trigger_type: str, tradingsymbol: str, exchange: str, 
                       trigger_values: List[float], last_price: float, 
                       orders: List[Dict]) -> int:
        """
        Place a GTT (Good Till Triggered) order
        
        Args:
            trigger_type: 'single' or 'two-leg'
            tradingsymbol: Trading symbol of the instrument
            exchange: Exchange of the instrument
            trigger_values: List of trigger values (1 for single, 2 for two-leg)
            last_price: Last traded price of the instrument
            orders: List of orders to place when the trigger is hit
            
        Returns:
            int: GTT order ID
        """
        try:
            await self._check_rate_limit()
            return self.kite.place_gtt(
                trigger_type=trigger_type,
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                trigger_values=trigger_values,
                last_price=last_price,
                orders=orders
            )
        except KiteException as e:
            self._handle_kite_exception(e, "placing GTT order")
    
    async def get_gtts(self) -> List[Dict]:
        """Get all GTT orders"""
        try:
            await self._check_rate_limit()
            return self.kite.gtts()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching GTT orders")
    
    async def get_gtt(self, trigger_id: int) -> Dict:
        """Get details of a specific GTT order"""
        try:
            await self._check_rate_limit()
            return self.kite.gtt(trigger_id)
        except KiteException as e:
            self._handle_kite_exception(e, f"fetching GTT order {trigger_id}")
    
    async def modify_gtt(self, trigger_id: int, trigger_type: str, 
                        tradingsymbol: str, exchange: str, 
                        trigger_values: List[float], last_price: float, 
                        orders: List[Dict]) -> int:
        """Modify a GTT order"""
        try:
            await self._check_rate_limit()
            return self.kite.modify_gtt(
                trigger_id=trigger_id,
                trigger_type=trigger_type,
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                trigger_values=trigger_values,
                last_price=last_price,
                orders=orders
            )
        except KiteException as e:
            self._handle_kite_exception(e, f"modifying GTT order {trigger_id}")
    
    async def delete_gtt(self, trigger_id: int) -> Dict:
        """Delete a GTT order"""
        try:
            await self._check_rate_limit()
            return self.kite.delete_gtt(trigger_id)
        except KiteException as e:
            self._handle_kite_exception(e, f"deleting GTT order {trigger_id}")
    
    # ========== Mutual Funds ==========
    
    async def get_mf_orders(self) -> List[Dict]:
        """Get all mutual fund orders"""
        try:
            await self._check_rate_limit()
            return self.kite.mf_orders()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching MF orders")
    
    async def place_mf_order(self, tradingsymbol: str, transaction_type: str, 
                           amount: float, amount_tag: str = None, 
                           folio: str = None) -> Dict:
        """Place a mutual fund order"""
        try:
            await self._check_rate_limit()
            return self.kite.place_mf_order(
                tradingsymbol=tradingsymbol,
                transaction_type=transaction_type,
                amount=amount,
                amount_tag=amount_tag,
                folio=folio
            )
        except KiteException as e:
            self._handle_kite_exception(e, "placing MF order")
    
    async def cancel_mf_order(self, order_id: str) -> Dict:
        """Cancel a mutual fund order"""
        try:
            await self._check_rate_limit()
            return self.kite.cancel_mf_order(order_id)
        except KiteException as e:
            self._handle_kite_exception(e, f"canceling MF order {order_id}")
    
    async def get_mf_holdings(self) -> List[Dict]:
        """Get mutual fund holdings"""
        try:
            await self._check_rate_limit()
            return self.kite.mf_holdings()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching MF holdings")
    
    async def get_mf_instruments(self) -> List[Dict]:
        """Get list of all mutual fund instruments"""
        try:
            await self._check_rate_limit()
            return self.kite.mf_instruments()
        except KiteException as e:
            self._handle_kite_exception(e, "fetching MF instruments")
            return self.kite.orders()
        except Exception as e:
            logger.error(f"Error getting orders: {str(e)}")
            raise

    def get_historical_data(self, instrument_token: int, from_date: datetime, 
                          to_date: datetime, interval: str) -> List[Dict]:
        """Get historical data for an instrument"""
        try:
            return self.kite.historical_data(
                instrument_token=instrument_token,
                from_date=from_date,
                to_date=to_date,
                interval=interval
            )
        except Exception as e:
            logger.error(f"Error getting historical data: {str(e)}")
            raise

    def get_instruments(self) -> List[Dict]:
        """Get all instruments"""
        try:
            return self.kite.instruments()
        except Exception as e:
            logger.error(f"Error getting instruments: {str(e)}")
            raise 