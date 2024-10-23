from typing import List, Dict
from models.skin_deal import SkinDeal
import numpy as np
from datetime import datetime, timedelta

class MarketAnalyzer:
    def __init__(self):
        self.price_trends: Dict[str, List[float]] = {}
        self.volume_trends: Dict[str, List[int]] = {}
        
    def analyze_deal(self, deal: SkinDeal) -> dict:
        """Comprehensive deal analysis"""
        analysis = {
            'profit_potential': deal.profit_potential,
            'risk_score': deal.risk_score,
            'recommendation': self._get_recommendation(deal),
            'market_strength': self._analyze_market_strength(deal),
            'price_stability': self._calculate_price_stability(deal),
            'investment_rating': self._calculate_investment_rating(deal)
        }
        
        return analysis
    
    def _get_recommendation(self, deal: SkinDeal) -> str:
        if not deal.market_metrics:
            return "Insufficient data"
            
        profit_ratio = deal.profit_potential / deal.price
        
        if profit_ratio > 0.3 and deal.risk_score < 0.3:
            return "Strong Buy"
        elif profit_ratio > 0.2 and deal.risk_score < 0.5:
            return "Buy"
        elif profit_ratio > 0.1 and deal.risk_score < 0.7:
            return "Consider"
        else:
            return "Pass"
            
    def _analyze_market_strength(self, deal: SkinDeal) -> float:
        if not deal.market_metrics:
            return 0.5
            
        volume_score = min(1.0, deal.market_metrics.volume_24h / 100)
        velocity_score = min(1.0, deal.market_metrics.sales_velocity / 5)
        
        return (volume_score * 0.6) + (velocity_score * 0.4)
        
    def _calculate_price_stability(self, deal: SkinDeal) -> float:
        if not deal.price_history or not deal.price_history.prices:
            return 0.5
            
        prices = np.array(deal.price_history.prices)
        return 1 - min(1.0, np.std(prices) / np.mean(prices))
        
    def _calculate_investment_rating(self, deal: SkinDeal) -> float:
        profit_score = min(1.0, deal.profit_potential / (deal.price * 0.5))
        risk_inverse = 1 - deal.risk_score
        market_strength = self._analyze_market_strength(deal)
        stability = self._calculate_price_stability(deal)
        
        weights = [0.4, 0.3, 0.2, 0.1]
        scores = [profit_score, risk_inverse, market_strength, stability]
        
        return sum(w * s for w, s in zip(weights, scores))