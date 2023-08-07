import telegram
from dexscreener import get_message_from_dexscreener
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


async def send_telegram_message(data):
    bot = telegram.Bot(token=TELEGRAM_KEY)
    await bot.send_message(chat_id=CHAT_ID, text=data)


async def send_daily_stats():
    message = await get_message_from_dexscreener()
    await send_telegram_message(message)
