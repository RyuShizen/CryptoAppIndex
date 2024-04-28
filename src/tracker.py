import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import asyncio
from discord.ext import commands, tasks
from utilities import evaluate_sentiment, weighted_average_sentiment_calculation
from data_management.database import AppRankTracker
import discord
import json
import time
import os
import schedule

class RankTracker:
    def __init__(self, bot):
        self.bot = bot
        self.url_coinbase = "https://apps.apple.com/us/app/coinbase-buy-sell-bitcoin/id886427730"
        self.url_coinbase_wallet = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
        self.url_binance = "https://apps.apple.com/us/app/binance-us-buy-bitcoin-eth/id1492670702"
        self.url_cryptodotcom = "https://apps.apple.com/us/app/crypto-com-buy-bitcoin-sol/id1262148500"

    def fetch_rank(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
            rank_text = rank_element.get_text(strip=True)
            rank_number = int(''.join(filter(str.isdigit, rank_text)))
            return rank_number
        except Exception as e:
            print(f"Error fetching rank: {e}")
            return None

    def fetch_coinbase_rank(self):
        return self.fetch_rank(self.url_coinbase)

    def fetch_coinbase_wallet_rank(self):
        return self.fetch_rank(self.url_coinbase_wallet)
    
    def fetch_binance_rank(self):
        return self.fetch_rank(self.url_binance)
    
    def fetch_cryptodotcom_rank(self):
        return self.fetch_rank(self.url_cryptodotcom)

    def save_rank_to_history(self, app_name, rank):
        now = datetime.now(timezone.utc)
        data_path = 'data/app_ranks.json'
        try:
            if os.path.exists(data_path):
                with open(data_path, 'r') as file:
                    data = json.load(file)
            else:
                data = {}

            data[app_name] = {
                'rank': rank,
                'timestamp': now.isoformat()
            }

            with open(data_path, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error while saving rank data: {e}")

    async def track_rank(self):
        coinbase_rank = self.fetch_coinbase_rank()
        if coinbase_rank is not None:
            print(f"Fetched Coinbase rank: {coinbase_rank}")
            self.save_rank_to_history('coinbase', coinbase_rank)
        else:
            print("Failed to fetch Coinbase rank.")

        coinbase_wallet_rank = self.fetch_coinbase_wallet_rank()
        if coinbase_wallet_rank is not None:
            print(f"Fetched Coinbase Wallet rank: {coinbase_wallet_rank}")
            self.save_rank_to_history("wallet", coinbase_wallet_rank)
        else:
            print("Failed to fetch Coinbase Wallet rank.")

        binance_rank = self.fetch_binance_rank()
        if binance_rank is not None:
            print(f"Fetched Binance rank: {binance_rank}")
            self.save_rank_to_history("binance", binance_rank)
        else:
            print("Failed to fetch Binance rank.")

        cryptodotcom_rank = self.fetch_cryptodotcom_rank()
        if cryptodotcom_rank is not None:
            print(f"Fetched Crypto.com rank: {cryptodotcom_rank}")
            self.save_rank_to_history("crypto.com", cryptodotcom_rank)
        else:
            print("Failed to fetch Crypto.com rank.")

    def get_current_rank(self, app_name):
        file_path = 'data/app_ranks.json'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if app_name in data:
                    return data[app_name]['rank']
        except IOError as e:
            print(f"Error accessing file {file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
        return None

    async def check_alerts(self):
        print("Checking alerts...")
        try:
            with open('data/alerts.json', 'r') as f:
                alerts = json.load(f)
        except IOError as e:
            print(f"Failed to read alerts file: {e}")
            return
        
        current_ranks = {
            'coinbase': self.get_current_rank('coinbase'),
            'wallet': self.get_current_rank('wallet'),
            'binance': self.get_current_rank('binance'),
            'cryptodotcom': self.get_current_rank('cryptodotcom')
        }

        for alert in alerts:
            user_id = alert['user_id']
            app = alert['app_name']
            current_rank = current_ranks.get(app, None)
            if current_rank and eval(f"{current_rank} {alert['operator']} {alert['rank']}"):
                await self.send_alert(user_id, app, current_rank)

        print("Alert checking completed.")

    async def send_alert(self, user_id, app_name, rank):

        # Create instances
        coinbase_tracker = AppRankTracker('Coinbase', 'data/rank_data_coinbase.json')
        wallet_tracker = AppRankTracker('Wallet', 'data/rank_data_wallet.json')
        binance_tracker = AppRankTracker('Binance', 'data/rank_data_binance.json')
        cryptodotcom_tracker = AppRankTracker('Crypto.com', 'data/rank_data_cryptodotcom.json')

        sentiment_text, sentiment_image_filename = evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker)
        average_sentiment_calculation = weighted_average_sentiment_calculation()

        try:
            user = await self.bot.fetch_user(user_id)
            if user:
                embed = discord.Embed(title=f"📢🔔 Alert for {app_name.capitalize()}!",
                                    description=f"The rank condition for **``{app_name.capitalize()}``** has been met! Current rank is **``{rank}``**.",
                                    color=0x00ff00)
                
                embed.add_field(name="Current Market Sentiment:", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``\n", inline=False)
                # Attach the sentiment image
                file_sentiment = discord.File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
                embed.set_image(url=f"attachment://{sentiment_image_filename}")

                embed.set_footer(text=f"Alert requested by {user.display_name}", icon_url=user.avatar.url if user.avatar else discord.Embed.Empty)

                await user.send(files=[file_sentiment], embed=embed)
                print(f"Alert sent to {user.display_name}")
            else:
                print(f"User {user_id} not found.")
        except discord.HTTPException as e:
            print(f"Failed to send message to {user_id}: {e}")

    async def update_bot_status(self):
        app_urls = [
            ("coinbase", self.url_coinbase),
            ("coinbase wallet", self.url_coinbase_wallet),
            ("binance", self.url_binance),
            ("crypto.com", self.url_cryptodotcom)
        ]
        status_index = 0
        while True:  # This loop will continuously update the status
            app_name, url = app_urls[status_index]
            rank = self.fetch_rank(url)
            if rank is not None:
                status_message = f"{app_name.capitalize()}: Rank #{rank}"
                await self.bot.change_presence(activity=discord.Game(name=status_message))
                print(f"Status updated: {status_message}")
            else:
                print(f"Failed to fetch rank for {app_name}")

            # Wait for some time before changing the status
            await asyncio.sleep(10)  # Change status every 10 seconds

            # Move to the next app status or loop back to the start
            status_index = (status_index + 1) % len(app_urls)


    def setup_schedule(self):
        schedule.every().hour.do(self.track_rank)
        schedule.every().hour.do(self.check_alerts)

    async def run(self):
        while True:
            await self.track_rank()
            await self.check_alerts()
            await self.update_bot_status()
            await asyncio.sleep(60)  # wait for x seconds
            
if __name__ == "__main__":
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
    tracker = RankTracker(bot)
