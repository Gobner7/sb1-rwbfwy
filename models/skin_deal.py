from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class PriceHistory:
    timestamps: List[datetime]
    prices: List[float]
    
    def get_trend(self) -> float:
        """Calculate price trend coefficient"""
        if len(self.prices) < 2:
            return 0.0
        return (self.prices[-1] - self.prices[0]) / len(self.prices)

@dataclass
class MarketMetrics:
    volume_24h: int
    sales_velocity: float  # Items sold per hour
    avg_time_to_sell: float
    volatility: float

@dataclass
class SkinDeal:
    name: str
    price: float
    market_price: float
    discount: float
    url: str
    site: str
    image_url: str
    wear_value: Optional[float] = None
    stickers: List[str] = None
    pattern_index: Optional[int] = None
    price_history: Optional[PriceHistory] = None
    market_metrics: Optional[MarketMetrics] = None
    
    @property
    def profit_potential(self) -> float:
        """Calculate potential profit considering market metrics"""
        base_profit = self.market_price - self.price
        if not self.market_metrics:
            return base_profit
            
        # Adjust profit based on market metrics
        velocity_factor = min(1.5, max(0.5, self.market_metrics.sales_velocity / 10))
        volatility_penalty = self.market_metrics.volatility * 0.2
        
        return base_profit * velocity_factor * (1 - volatility_penalty)
    
    @property
    def risk_score(self) -> float:
        """Calculate risk score (0-1, lower is better)"""
        if not self.market_metrics:
            return 0.5
            
        risk = 0.0
        # Higher volatility means higher risk
        risk += self.market_metrics.volatility * 0.3
        # Longer sell time means higher risk
        risk += min(0.3, self.market_metrics.avg_time_to_sell / 72) * 0.4
        # Lower volume means higher risk
        risk += max(0.0, 1 - (self.market_metrics.volume_24h / 50)) * 0.3
        
        return min(1.0, risk)