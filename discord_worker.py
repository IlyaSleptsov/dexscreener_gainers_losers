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
    embed = discord.Embed()


    @discord_client.event
    async def on_ready():
        print(f'{discord_client.user.name} has connected to Discord!')

    @discord_client.event
    async def on_message(message):
        if '/get_daily_stats' in message.content.lower():
            gainers_message = await get_message_from_dexscreener(discord=True)
            embed.description = gainers_message
            await message.channel.send(embed=embed)

    await discord_client.start(DISCORD_TOKEN)

