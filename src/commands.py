from api.coinbase import current_rank_coinbase, current_rank_wallet
from utilities import number_to_emoji, evaluate_sentiment
from data_management.database import AppRankTracker
from utilities import number_to_emoji
from datetime import datetime
import discord

coinbase_tracker = AppRankTracker('Coinbase', 'data/rank_data_coinbase.json')
wallet_tracker = AppRankTracker('Wallet', 'data/rank_data_wallet.json')

async def coinbase(ctx):

    rank_number_coinbase = current_rank_coinbase()

    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    sentiment_evaluation = evaluate_sentiment(coinbase_tracker, wallet_tracker)  # Assuming wallet_tracker is also defined
    change_symbol = coinbase_tracker.compare_ranks(rank_number_coinbase)
    highest_rank, lowest_rank = coinbase_tracker.get_extreme_ranks()

    embed = discord.Embed(title="📲 Coinbase App Ranking", description="Real-time tracking and analysis of the Coinbase app ranking.", color=0x00ff00)

    # URL must be a publicly accessible link
    file = discord.File("assets\CoinbaseRankBot_logo.png", filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")

    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{number_to_emoji(rank_number_coinbase)} in Finance on {current_datetime_hour}``", inline=False)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
    
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    embed.add_field(name="⛅ Market Sentiment", value=sentiment_evaluation, inline=False)
    embed.add_field(name="📆 Last Updated", value=datetime.now().strftime('``%Y-%m-%d at %H:%M:%S``'), inline=False)

    coinbase_tracker.save_rank(rank_number_coinbase)

    await ctx.send(file=file, embed=embed)

async def cwallet(ctx):

    rank_number_wallet = current_rank_wallet()  # Ensure you have a function that fetches the current rank for Wallet

    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')
    rank_number_emoji = number_to_emoji(rank_number_wallet)
    
    embed = discord.Embed(
        title="📲 Coinbase Wallet App Ranking",
        description="Real-time tracking and analysis of the Coinbase Wallet app ranking.",
        color=0x00ff00
    )
    
    # Assuming the logo URL is publicly accessible
    file = discord.File("assets\CoinbaseRankBot_logo.png", filename="image.png")
    embed.set_thumbnail(url="attachment://image.png")

    embed.add_field(name="🏆 Current Rank", value=f"``#️⃣{rank_number_emoji} in Finance on {current_datetime_hour}``", inline=False)
    change_symbol = wallet_tracker.compare_ranks(rank_number_wallet)
    embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)

    highest_rank, lowest_rank = wallet_tracker.get_extreme_ranks()
    if highest_rank:
        embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"``#️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}``", inline=True)
    if lowest_rank:
        embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"``#️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}``", inline=True)

    sentiment_evaluation = evaluate_sentiment(coinbase_tracker, wallet_tracker)  # Assuming wallet_tracker is also defined
    embed.add_field(name="⛅ Market Sentiment", value=sentiment_evaluation, inline=False)
    embed.add_field(name="📆 Last Updated", value=f"``{current_datetime_hour}``", inline=False)

    wallet_tracker.save_rank(rank_number_wallet)  # Assuming wallet_tracker is an instance of AppRankTracker

    await ctx.send(file=file, embed=embed)

def setup_commands(bot):
    bot.command(name='coinbase')(coinbase)
    bot.command(name='cwallet')(cwallet)
