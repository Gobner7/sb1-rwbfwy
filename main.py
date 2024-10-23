import asyncio
import logging
from typing import List
from models.skin_deal import SkinDeal
from scrapers.buff_scraper import BuffScraper
from analysis.market_analyzer import MarketAnalyzer
from notifications.discord_notifier import DiscordNotifier
from dotenv import load_dotenv
import os
import json
from datetime import datetime

class CS2MarketBot:
    def __init__(self):
        load_dotenv()
        self.webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.setup_logging()
        
        self.scrapers = [BuffScraper()]  # Add more scrapers here
        self.analyzer = MarketAnalyzer()
        self.notifier = DiscordNotifier(self.webhook_url)
        
        # Deal tracking
        self.seen_deals = set()
        self.deal_history = []
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('market_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CS2MarketBot')
        
    async def fetch_all_deals(self) -> List[SkinDeal]:
        all_deals = []
        for scraper in self.scrapers:
            try:
                deals = await scraper.fetch_listings()
                all_deals.extend(deals)
            except Exception as e:
                self.logger.error(f"Error with scraper {scraper.__class__.__name__}: {str(e)}")
        return all_deals
        
    def filter_deals(self, deals: List[SkinDeal]) -> List[SkinDeal]:
        filtered_deals = []
        for deal in deals:
            # Skip if we've seen this deal recently
            deal_key = f"{deal.site}:{deal.name}:{deal.price}"
            if deal_key in self.seen_deals:
                continue
                
            analysis = self.analyzer.analyze_deal(deal)
            
            # Advanced filtering criteria
            if (deal.profit_potential > 5.0 and  # Minimum $5 profit
                deal.risk_score < 0.7 and        # Maximum risk threshold
                analysis['investment_rating'] > 0.6):  # Minimum investment rating
                
                filtered_deals.append(deal)
                self.seen_deals.add(deal_key)
                
        return filtered_deals
        
    def save_deal_history(self):
        """Save deal history to JSON for analysis"""
        history_data = {
            'timestamp': datetime.now().isoformat(),
            'deals': [
                {
                    'name': deal.name,
                    'price': deal.price,
                    'market_price': deal.market_price,
                    'profit_potential': deal.profit_potential,
                    'risk_score': deal.risk_score,
                    'site': deal.site
                }
                for deal in self.deal_history[-1000:]  # Keep last 1000 deals
            ]
        }
        
        with open('deal_history.json', 'w') as f:
            json.dump(history_data, f, indent=2)
        
    async def monitor_markets(self):
        self.logger.info("Starting CS2 Market Bot...")
        
        while True:
            try:
                # Fetch and analyze deals
                all_deals = await self.fetch_all_deals()
                good_deals = self.filter_deals(all_deals)
                
                # Update deal history
                self.deal_history.extend(good_deals)
                if len(self.deal_history) > 1000:
                    self.deal_history = self.deal_history[-1000:]
                
                # Save history periodically
                self.save_deal_history()
                
                # Send notifications for good deals
                for deal in good_deals:
                    self.notifier.send_deal_notification(deal)
                
                # Clear old deals from seen_deals set periodically
                if len(self.seen_deals) > 10000:
                    self.seen_deals.clear()
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Error in market monitoring: {str(e)}")
                await asyncio.sleep(30)

if __name__ == "__main__":
    bot = CS2MarketBot()
    
    try:
        asyncio.run(bot.monitor_markets())
    except KeyboardInterrupt:
        bot.logger.info("\nBot stopped by user")
    except Exception as e:
        bot.logger.error(f"Fatal error: {str(e)}")