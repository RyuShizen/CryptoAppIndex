import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
from datetime import datetime

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

def save_rank_coinbase(rank_number):
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d %H')
    
    try:
        with open('rank_data_coinbase.json', 'r') as f:
            data = json.load(f)

        last_datetime_hour = data['date'][:13]
        need_to_update = last_datetime_hour != current_datetime_hour
    except (FileNotFoundError, json.JSONDecodeError):
        need_to_update = True
        data = {
            'last_rank': None, 
            'date': now.strftime('%Y-%m-%d %H:%M:%S'),
            'highest_rank': {'rank': None, 'timestamp': ''},
            'lowest_rank': {'rank': None, 'timestamp': ''}
        }

    if need_to_update:
        rank_number = int(rank_number)

        if data['highest_rank']['rank'] is None or rank_number < data['highest_rank']['rank']:
            data['highest_rank'] = {'rank': rank_number, 'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')}
        if data['lowest_rank']['rank'] is None or rank_number > data['lowest_rank']['rank']:
            data['lowest_rank'] = {'rank': rank_number, 'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')}

        data['last_rank'] = rank_number
        data['date'] = now.strftime('%Y-%m-%d %H:%M:%S')

        with open('rank_data_coinbase.json', 'w') as f:
            json.dump(data, f, indent=4)

def save_rank_wallet(rank_number):
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d %H')
    
    try:
        with open('rank_data_wallet.json', 'r') as f:
            data = json.load(f)

        last_datetime_hour = data['date'][:13]
        need_to_update = last_datetime_hour != current_datetime_hour
    except (FileNotFoundError, json.JSONDecodeError):
        need_to_update = True
        data = {
            'last_rank': None, 
            'date': now.strftime('%Y-%m-%d %H:%M:%S'),
            'highest_rank': {'rank': None, 'timestamp': ''},
            'lowest_rank': {'rank': None, 'timestamp': ''}
        }

    if need_to_update:
        rank_number = int(rank_number)

        if data['highest_rank']['rank'] is None or rank_number < data['highest_rank']['rank']:
            data['highest_rank'] = {'rank': rank_number, 'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')}
        if data['lowest_rank']['rank'] is None or rank_number > data['lowest_rank']['rank']:
            data['lowest_rank'] = {'rank': rank_number, 'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')}

        data['last_rank'] = rank_number
        data['date'] = now.strftime('%Y-%m-%d %H:%M:%S')

        with open('rank_data_wallet.json', 'w') as f:
            json.dump(data, f, indent=4)

def get_extreme_ranks_coinbase():
    try:
        with open('rank_data_coinbase.json', 'r') as f:
            data = json.load(f)
        highest_rank_coinbase = data.get('highest_rank', {})
        lowest_rank_coinbase = data.get('lowest_rank', {})
        return highest_rank_coinbase, lowest_rank_coinbase
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_extreme_ranks_wallet():
    try:
        with open('rank_data_wallet.json', 'r') as f:
            data = json.load(f)
        highest_rank_wallet = data.get('highest_rank', {})
        lowest_rank_wallet = data.get('lowest_rank', {})
        return highest_rank_wallet, lowest_rank_wallet
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_previous_rank_coinbase():
    try:
        with open('rank_data_coinbase.json', 'r') as f:
            data = json.load(f)
        return data.get('last_rank', None), data.get('date', 'No date found')
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_previous_rank_wallet():
    try:
        with open('rank_data_wallet.json', 'r') as f:
            data = json.load(f)
        return data.get('last_rank', None), data.get('date', 'No date found')
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_date_from_json_coinbase():
    try:
        with open('rank_data_coinbase.json', 'r') as f:
            data = json.load(f)
        date_value = data.get('date', 'No date found')
        return date_value
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        return 'No date found'

def get_date_from_json_wallet():
    try:
        with open('rank_data_wallet.json', 'r') as f:
            data = json.load(f)
        date_value = data.get('date', 'No date found')
        return date_value
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        return 'No date found'

def compare_ranks_coinbase(current_rank_coinbase):
    previous_rank_coinbase, _ = get_previous_rank_coinbase()
    last_rank_date_coinbase = get_date_from_json_coinbase()

    if previous_rank_coinbase is None:
        return "Rank data not available for comparison."

    current_rank_coinbase = int(current_rank_coinbase)
    previous_rank_coinbase = int(previous_rank_coinbase)

    if current_rank_coinbase == previous_rank_coinbase:
        return f"💤 (No Change)."
    elif current_rank_coinbase < previous_rank_coinbase:
        return f"🔼 Increased by +{previous_rank_coinbase - current_rank_coinbase} position(s) since {last_rank_date_coinbase}"
    else:
        return f"🔻 Decreased by -{current_rank_coinbase - previous_rank_coinbase} position(s) since {last_rank_date_coinbase}"

def compare_ranks_wallet(current_rank_wallet):
    previous_rank_wallet, _ = get_previous_rank_wallet()
    last_rank_date_wallet = get_date_from_json_wallet()

    if previous_rank_wallet is None:
        return "Rank data not available for comparison."

    current_rank_wallet = int(current_rank_wallet)
    previous_rank_wallet = int(previous_rank_wallet)

    if current_rank_wallet == previous_rank_wallet:
        return f"💤 (No Change)."
    elif current_rank_wallet < previous_rank_wallet:
        return f"🔼 Increased by +{previous_rank_wallet - current_rank_wallet} position(s) since {last_rank_date_wallet}"
    else:
        return f"🔻 Decreased by -{current_rank_wallet - previous_rank_wallet} position(s) since {last_rank_date_wallet}"

    
def evaluate_sentiment(current_rank_coinbase, current_rank_wallet):
    
    try:
        current_rank_coinbase = int(current_rank_coinbase)
        current_rank_wallet = int(current_rank_wallet)
    except ValueError:
        raise ValueError("Les rangs doivent être des entiers")
    
    weighted_average_rank = (2 * current_rank_coinbase + current_rank_wallet) / 3

    if weighted_average_rank <= 3:
        sentiment = "🟢🟢🟢 **Extreme Greed!!!**"
    elif weighted_average_rank <= 10:
        sentiment = "🟢🟢 **Greed!**"
    elif weighted_average_rank <= 20:
        sentiment = "🟢 **Belief.**"
    elif weighted_average_rank <= 30:
        sentiment = "🟡 **Optimism.**"
    elif weighted_average_rank <= 45:
        sentiment = "🟡🟠 **Anxiety.**"
    elif weighted_average_rank <= 60:
        sentiment = "🟠🟠 **Fear.**"
    else:
        sentiment = "🔴 **Capitulation.**"

    return f"🚥 Sentiment Indicator (*Weighted Average*): {sentiment}"

def current_rank_coinbase():
    url = "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number_coinbase = ''.join(filter(str.isdigit, rank_text))
    return rank_number_coinbase

def current_rank_wallet():
    url = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number_wallet = ''.join(filter(str.isdigit, rank_text))
    return rank_number_wallet

def number_to_emoji(number):
    
    digit_to_emoji = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '9': '9️⃣'
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def coinbase(ctx):
    url = "https://apps.apple.com/us/app/coinbase-buy-bitcoin-ether/id886427730"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number_coinbase = ''.join(filter(str.isdigit, rank_text))
        rank_number_emoji = number_to_emoji(rank_number_coinbase)

        message_title = "📊 **Coinbase App Ranking** 📊\n"
        message_rank = f"🏆 Current Rank: #️⃣{rank_number_emoji} in Finance on {current_datetime_hour}."

        rank_number_coinbase = current_rank_coinbase()
        rank_number_wallet = current_rank_wallet()
        sentiment_evaluation = evaluate_sentiment(rank_number_coinbase, rank_number_wallet)
        change_symbol = compare_ranks_coinbase(rank_number_coinbase)
               
        highest_rank, lowest_rank = get_extreme_ranks_coinbase()
        recent_change = f"🔂 Recent Positional Change: {change_symbol}"
        last_updated = f"📅 **Last Updated:** {current_datetime_hour}."
        highest_rank_msg = f"📈 Peak Rank Achieved (ATH): #️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}." if highest_rank else "Highest rank data not available."
        lowest_rank_msg = f"📉 Recent Lowest Rank (ATL): #️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}." if lowest_rank else "Lowest rank data not available."
        
        save_rank_coinbase(rank_number_coinbase)

        await ctx.send(f"{message_title}\n{message_rank}\n{recent_change}\n\n**Achievements & Records:**\n\n{highest_rank_msg}\n{lowest_rank_msg}\n\n**Market Sentiment:**\n\n{sentiment_evaluation}\n\n{last_updated}")
    else:
        await ctx.send("Rank could not be found.")

@bot.command()
async def cwallet(ctx):
    url = "https://apps.apple.com/us/app/coinbase-wallet-nfts-crypto/id1278383455"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number_wallet = ''.join(filter(str.isdigit, rank_text))
        rank_number_emoji = number_to_emoji(rank_number_wallet)

        message_title = "📊 **Coinbase Wallet App Ranking** 📊\n"
        message_rank = f"🏆 Current Rank: #️⃣{rank_number_emoji} in Finance on {current_datetime_hour}."

        rank_number_coinbase = current_rank_coinbase()
        rank_number_wallet = current_rank_wallet()
        sentiment_evaluation = evaluate_sentiment(rank_number_coinbase, rank_number_wallet)
        change_symbol = compare_ranks_wallet(rank_number_wallet)
               
        highest_rank, lowest_rank = get_extreme_ranks_wallet()
        recent_change = f"🔂 Recent Positional Change: {change_symbol}"
        last_updated = f"📅 **Last Updated:** {current_datetime_hour}."
        highest_rank_msg = f"📈 Peak Rank Achieved (ATH): #️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}." if highest_rank else "Highest rank data not available."
        lowest_rank_msg = f"📉 Recent Lowest Rank (ATL): #️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}." if lowest_rank else "Lowest rank data not available."
        
        save_rank_wallet(rank_number_wallet)

        await ctx.send(f"{message_title}\n{message_rank}\n{recent_change}\n\n**Achievements & Records:**\n\n{highest_rank_msg}\n{lowest_rank_msg}\n\n**Market Sentiment:**\n\n{sentiment_evaluation}\n\n{last_updated}")
    else:
        await ctx.send("Rank could not be found.")

bot.run(bot_token)
