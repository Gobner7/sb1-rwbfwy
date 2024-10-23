from abc import ABC, abstractmethod
from typing import List, Optional
from models.skin_deal import SkinDeal
import stealth_requests as requests
import asyncio
import logging

class BaseScraper(ABC):
    def __init__(self):
        self.session = requests.StealthSession(impersonate='chrome')
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    async def fetch_listings(self) -> List[SkinDeal]:
        pass
        
    @abstractmethod
    async def fetch_price_history(self, item_id: str) -> Optional[List[float]]:
        pass
        
    @abstractmethod
    async def fetch_market_metrics(self, item_id: str) -> Optional[dict]:
        pass
        
    async def delay_request(self):
        """Implement random delays between requests"""
        delay = random.uniform(1.5, 4.0)
        await asyncio.sleep(delay)