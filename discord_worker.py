import discord
from dexscreener import get_message_from_dexscreener
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


async def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    discord_client = discord.Client(intents=intents)

    @discord_client.event
    async def on_ready():
        print(f'{discord_client.user.name} has connected to Discord!')

    @discord_client.event
    async def on_message(message):
        if '/get_daily_stats' in message.content.lower():
            stats_message = await get_message_from_dexscreener()
            await message.channel.send(stats_message)

    await discord_client.start(DISCORD_TOKEN)
