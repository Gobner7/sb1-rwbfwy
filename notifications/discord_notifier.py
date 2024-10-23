from discord_webhook import DiscordWebhook, DiscordEmbed
from models.skin_deal import SkinDeal
from analysis.market_analyzer import MarketAnalyzer
import logging
from datetime import datetime

class DiscordNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.logger = logging.getLogger('DiscordNotifier')
        self.analyzer = MarketAnalyzer()
        
    def send_deal_notification(self, deal: SkinDeal):
        try:
            analysis = self.analyzer.analyze_deal(deal)
            
            webhook = DiscordWebhook(url=self.webhook_url)
            embed = DiscordEmbed(
                title=f"💎 Premium Deal Alert: {deal.name}",
                description=self._generate_description(deal, analysis),
                color=self._get_color(analysis)
            )
            
            # Main deal info
            embed.add_embed_field(name="💰 Price", value=f"${deal.price:.2f}", inline=True)
            embed.add_embed_field(name="📊 Market", value=f"${deal.market_price:.2f}", inline=True)
            embed.add_embed_field(name="📉 Discount", value=f"{deal.discount:.1f}%", inline=True)
            
            # Advanced metrics
            embed.add_embed_field(name="📈 Profit Potential", 
                                value=f"${deal.profit_potential:.2f}", inline=True)
            embed.add_embed_field(name="⚠️ Risk Score", 
                                value=f"{deal.risk_score:.2f}", inline=True)
            embed.add_embed_field(name="⭐ Investment Rating", 
                                value=f"{analysis['investment_rating']:.2f}/1.0", inline=True)
            
            # Market metrics if available
            if deal.market_metrics:
                embed.add_embed_field(name="📊 Market Metrics", 
                    value=f"Volume: {deal.market_metrics.volume_24h}/24h\n"
                          f"Velocity: {deal.market_metrics.sales_velocity:.1f}/h\n"
                          f"Avg. Sell Time: {deal.market_metrics.avg_time_to_sell:.1f}h",
                    inline=False)
            
            # Special attributes
            if deal.wear_value or deal.stickers or deal.pattern_index:
                special_attrs = []
                if deal.wear_value:
                    special_attrs.append(f"Wear: {deal.wear_value:.4f}")
                if deal.stickers:
                    special_attrs.append(f"Stickers: {len(deal.stickers)}")
                if deal.pattern_index:
                    special_attrs.append(f"Pattern: #{deal.pattern_index}")
                    
                embed.add_embed_field(name="🔍 Special Attributes",
                                    value=" | ".join(special_attrs),
                                    inline=False)
            
            embed.add_embed_field(name="🔗 Quick Buy",
                                value=f"[Buy on {deal.site}]({deal.url})",
                                inline=False)
            
            embed.set_thumbnail(url=deal.image_url)
            embed.set_footer(text=f"CS2 Market Bot • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            webhook.add_embed(embed)
            webhook.execute()
            
        except Exception as e:
            self.logger.error(f"Error sending Discord notification: {str(e)}")
            
    def _generate_description(self, deal: SkinDeal, analysis: dict) -> str:
        return (
            f"**Recommendation: {analysis['recommendation']}**\n"
            f"Market Strength: {analysis['market_strength']:.2f}/1.0\n"
            f"Price Stability: {analysis['price_stability']:.2f}/1.0\n"
        )
        
    def _get_color(self, analysis: dict) -> int:
        if analysis['recommendation'] == "Strong Buy":
            return 0x00ff00  # Green
        elif analysis['recommendation'] == "Buy":
            return 0x00cc00  # Light green
        elif analysis['recommendation'] == "Consider":
            return 0xffff00  # Yellow
        else:
            return 0xff0000  # Red