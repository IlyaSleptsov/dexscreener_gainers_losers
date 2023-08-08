import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from telegram_worker import send_daily_stats
from discord_worker import run_discord_bot


async def make_schedule():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_daily_stats, 'cron', hours="22")
    scheduler.start()


def main():
    loop = asyncio.get_event_loop()
    loop.create_task(make_schedule())
    loop.create_task(run_discord_bot())
    loop.run_forever()


if __name__ == '__main__':
    logging.basicConfig(format=u'[%(asctime)s] %(levelname).1s %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S',
                        filename='send_top_gainers_losers_logs',
                        filemode='a',
                        level=logging.INFO)
    try:
        main()
    except Exception as e:
        logging.exception(e)