from scrapers.base_scraper import BaseScraper
from models.skin_deal import SkinDeal, PriceHistory, MarketMetrics
import json
from datetime import datetime, timedelta
import random

class BuffScraper(BaseScraper):
    BASE_URL = "https://buff.163.com/api/market"
    
    async def fetch_listings(self) -> List[SkinDeal]:
        deals = []
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://buff.163.com/market/csgo',
            }
            
            # Fetch multiple pages for better coverage
            for page in range(1, 4):
                await self.delay_request()
                response = await self.session.get(
                    f"{self.BASE_URL}/goods",
                    params={'game': 'csgo', 'page': page},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for item in data['data']['items']:
                        # Fetch additional data
                        price_history = await self.fetch_price_history(item['id'])
                        market_metrics = await self.fetch_market_metrics(item['id'])
                        
                        deal = SkinDeal(
                            name=item['name'],
                            price=float(item['price']),
                            market_price=float(item['market_price']),
                            discount=float(item['discount']),
                            url=f"https://buff.163.com/goods/{item['id']}",
                            site="BUFF",
                            image_url=item['icon_url'],
                            wear_value=float(item.get('wear_value', 0)),
                            stickers=item.get('stickers', []),
                            pattern_index=item.get('pattern_index'),
                            price_history=price_history,
                            market_metrics=market_metrics
                        )
                        deals.append(deal)
                        
        except Exception as e:
            self.logger.error(f"Error fetching BUFF listings: {str(e)}")
            
        return deals