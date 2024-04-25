from discord.ext import commands
import discord
import json
import os
from datetime import datetime

# Import your necessary modules here
from api.apps import current_rank_coinbase, current_rank_wallet, current_rank_binance, current_rank_cryptodotcom
from utilities import number_to_emoji, evaluate_sentiment
from data_management.database import AppRankTracker

# Create tracker instances
coinbase_tracker = AppRankTracker('Coinbase', 'data/rank_data_coinbase.json')
wallet_tracker = AppRankTracker('Wallet', 'data/rank_data_wallet.json')
binance_tracker = AppRankTracker('Binance', 'data/rank_data_binance.json')
cryptodotcom_tracker = AppRankTracker('Crypto.com', 'data/rank_data_cryptodotcom.json')

# Setup a bot instance here if not passed from bot.py
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def coinbase(ctx):
    rank_number_coinbase = current_rank_coinbase()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume wallet_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker)
    change_symbol = coinbase_tracker.compare_ranks(rank_number_coinbase)
    highest_rank, lowest_rank = coinbase_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Coinbase Statistics", description="Real-time tracking and analysis of the Coinbase app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets\coinbase-coin-seeklogo.png", filename="coinbase_logo.png")
    embed.set_thumbnail(url="attachment://coinbase_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_coinbase)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"``{sentiment_text}``", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def cwallet(ctx):
    rank_number_wallet = current_rank_wallet()  # Ensure you have a function that fetches the current rank for Wallet
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume wallet_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker)
    change_symbol = wallet_tracker.compare_ranks(rank_number_wallet)
    highest_rank, lowest_rank = wallet_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Coinbase's Wallet Statistics", description="Real-time tracking and analysis of the Coinbase's Wallet app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets\coinbase-wallet-seeklogo.png", filename="coinbase_wallet_logo.png")
    embed.set_thumbnail(url="attachment://coinbase_wallet_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_wallet)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"``{sentiment_text}``", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def binance(ctx):
    rank_number_binance = current_rank_binance()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume binance_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker)
    change_symbol = binance_tracker.compare_ranks(rank_number_binance)
    highest_rank, lowest_rank = binance_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Binance Statistics", description="Real-time tracking and analysis of the Binance app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets/binance-smart-chain-bsc-seeklogo.png", filename="binance_logo.png")
    embed.set_thumbnail(url="attachment://binance_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_binance)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"``{sentiment_text}``", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

@bot.command()
async def cryptocom(ctx):
    rank_number_cryptodotcom = current_rank_cryptodotcom()
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    # Assume cryptodotcom_tracker is also defined
    sentiment_text, sentiment_image_filename = evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker)
    change_symbol = cryptodotcom_tracker.compare_ranks(rank_number_cryptodotcom)
    highest_rank, lowest_rank = cryptodotcom_tracker.get_extreme_ranks()

    embed = discord.Embed(title="Crypto.com Statistics", description="Real-time tracking and analysis of the Crypto.com app ranking.", color=0x00ff00)

    # Attach the main thumbnail
    file_thumb = discord.File("assets/crypto-com-seeklogo.png", filename="cryptodotcom_logo.png")
    embed.set_thumbnail(url="attachment://cryptodotcom_logo.png")

    # Add fields before Market Sentiment
    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_cryptodotcom)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    # Market Sentiment field and image below it
    embed.add_field(name="🚥 Market Sentiment", value=f"``{sentiment_text}``", inline=False)

    # Attach the sentiment image
    file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
    embed.set_image(url=f"attachment://{sentiment_image_filename}")

    # Footer and sending the message
    avatar_url = ctx.author.avatar.url if ctx.author.avatar else None
    embed.set_footer(text=f"Requested by {ctx.author.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else discord.Embed.Empty)

    await ctx.send(files=[file_thumb, file_sentiment], embed=embed)

def setup_commands(bot):
    bot.add_command(coinbase)
    bot.add_command(binance)
    bot.add_command(cryptocom)
    bot.add_command(cwallet)
