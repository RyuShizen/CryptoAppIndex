from discord.ext import commands
from config import BOT_TOKEN
from commands import setup_commands
import discord

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

setup_commands(bot)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run(BOT_TOKEN)