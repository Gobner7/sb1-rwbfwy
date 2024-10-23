# CS2 Market Analysis Bot

Advanced CS2 skin market analyzer that monitors multiple marketplaces for profitable deals and sends notifications to Discord.

## Features

- Multi-site monitoring (BUFF, Skinport)
- Stealth scraping to avoid detection
- Asynchronous requests for better performance
- Beautiful Discord embeds with detailed deal information
- Automatic deal filtering based on discount percentage
- Comprehensive error handling and logging
- Threading support for parallel processing

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Configure your Discord webhook URL in `.env` file

3. Run the bot:
```bash
python main.py
```

## Configuration

You can adjust the following parameters in `main.py`:
- Minimum discount percentage
- Minimum item price
- Scan interval
- Target marketplaces

## Security

The bot uses stealth requests to avoid detection:
- Browser fingerprint mimicking
- Request rate limiting
- Dynamic headers
- TLS fingerprint masking

## Logging

All activities are logged to `market_bot.log` for monitoring and debugging.