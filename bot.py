import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def coinbase(ctx):
    url = "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number = ''.join(filter(str.isdigit, rank_text))
        message = f"The rank of the Coinbase app on the App Store is : #{rank_number} in Finance."
    else:
        message = "Rank could not be found."
    
    await ctx.send(message)

bot.run(bot_token)

