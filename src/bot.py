from discord.ext import commands
from config import BOT_TOKEN
from commands import setup_commands
from tracker import RankTracker
import discord
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
setup_commands(bot)

tracker = RankTracker(bot)

def start_tracker():
    asyncio.new_event_loop().run_until_complete(tracker.run())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(tracker.run())

@bot.event
async def on_disconnect():
    print("Bot is disconnecting...")
    asyncio.run_coroutine_threadsafe(tracker.shutdown(), bot.loop)

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
