## Run
`poetry run python3 send_top_gainers_losers.py`

## About
### send_top_gainers_losers.py 
The main file that starts workers:
- schedules Telegram messages
- launches Discord bot that processes _/get_daily_stats_ command

We can easily add there more tasks (in asyncio loop) or scheduled jobs (in AsyncIOScheduler).
### dexscreener.py

A number of functions responsible for data parsing and formatting:
- _get_message_from_dexscreener()_ – main function
- _get_data(uri)_ – retrieves data from DexScreener
- _format_number(number)_ and _format_data_into_message(gainers_data, losers_data, limit)_ – data formatting

**Important point:** 
DexScreener utilizes socket API and doesn't introduce any data protection measures, 
so I use hard-coded headers and don't paste in request 
my secret key from web-interface (it is automatically generated and there is no need in it).

### telegram_worker.py
Two functions: to send Telegram messages and to ask data from dexscreener.py and send message. 

### discord_worker.py
_run_discord_bot()_ function to launch bot that is called from send_top_gainers_losers.py 
file and a decorator that processes _/get_daily_stats_ command.

## Possible improvements
1. We definitely need to add links in our stats message because you read it and want to tap. I found out a way how to generate a link and paste it in the text, can add in near time.
2. I don't see problems for now but we can add more processing of corner cases that can potentially arise.
3. I believe (if we find this useful) we can extract more insights from this data taking into account lower time periods (like, highlighting hot coins on 1 hour timeframe).