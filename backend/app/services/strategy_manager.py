from typing import Dict
import logging
from sqlalchemy.orm import Session

from app.models.strategy import Strategy
from app.services.strategy import StrategyService
from app.services.kite import KiteService

logger = logging.getLogger(__name__)

class StrategyManager:
    def __init__(self, db: Session):
        self.db = db
        self.active_strategies: Dict[int, StrategyService] = {}

    async def start_strategy(self, strategy: Strategy, kite_service: KiteService):
        if strategy.id in self.active_strategies:
            logger.warning(f"Strategy {strategy.id} is already running")
            return
        
        strategy_service = StrategyService(self.db, strategy, kite_service)
        await strategy_service.start()
        self.active_strategies[strategy.id] = strategy_service
        logger.info(f"Strategy {strategy.id} started")

    async def stop_strategy(self, strategy_id: int):
        if strategy_id not in self.active_strategies:
            logger.warning(f"Strategy {strategy_id} is not running")
            return
        
        strategy_service = self.active_strategies[strategy_id]
        await strategy_service.stop()
        del self.active_strategies[strategy_id]
        logger.info(f"Strategy {strategy_id} stopped")

    async def stop_all_strategies(self):
        for strategy_id in list(self.active_strategies.keys()):
            await self.stop_strategy(strategy_id)
        logger.info("All strategies stopped")

    def is_strategy_running(self, strategy_id: int) -> bool:
        return strategy_id in self.active_strategies

    def get_running_strategies(self) -> Dict[int, StrategyService]:
        return self.active_strategies.copy() 