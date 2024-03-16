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

from datetime import datetime
import json

def save_rank(rank_number):
    now = datetime.now()
    current_datetime_hour = now.strftime('%Y-%m-%d %H')
    
    try:
        with open('rank_data.json', 'r') as f:
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

        with open('rank_data.json', 'w') as f:
            json.dump(data, f, indent=4)


def get_extreme_ranks():
    try:
        with open('rank_data.json', 'r') as f:
            data = json.load(f)
        highest_rank = data.get('highest_rank', {})
        lowest_rank = data.get('lowest_rank', {})
        return highest_rank, lowest_rank
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_previous_rank():
    try:
        with open('rank_data.json', 'r') as f:
            data = json.load(f)
        return data['last_rank'], data['date']
    except (FileNotFoundError, json.JSONDecodeError):
        return None, None

def get_date_from_json():
    try:
        with open('rank_data.json', 'r') as f:
            data = json.load(f)
        date_value = data.get('date', 'No date found')
        return date_value
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading the JSON file: {e}")
        return 'No date found'

def compare_ranks(current_rank):
    previous_rank, _ = get_previous_rank()
    if previous_rank is None:
        return "Rank data not available for comparison."

    current_rank = int(current_rank)
    previous_rank = int(previous_rank)

    if current_rank == previous_rank:
        return f"💤 (No Change)."
    elif current_rank < previous_rank:
        return f"🔼 +{previous_rank - current_rank}."
    else:
        return f"🔻-{current_rank - previous_rank}."
    
def evaluate_sentiment(current_rank):
        
        current_rank = int(current_rank)

        if current_rank <= 3:
                sentiment = "🟢🟢🟢 Euphoria!!!"
        elif current_rank <= 10:
                sentiment = "🟢🟢 Greed!"
        elif current_rank <= 20:
                sentiment = "🟢 Belief."
        elif current_rank <= 50:
                sentiment = "🟡 Optimism/Anxiety."
        elif current_rank <= 75:
                sentiment = "🟠 Hope/Fear."
        else:
                sentiment = "🔴 Capitulation."

        return f"🚥 Sentiment : {sentiment}"

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

    rank_element = soup.find('a', class_='inline-list__item', href=True, text=lambda t: 'in Finance' in t)
    last_rank_date = get_date_from_json()

    if rank_element:
        rank_text = rank_element.get_text(strip=True)
        rank_number = ''.join(filter(str.isdigit, rank_text))
        rank_number_emoji = number_to_emoji(rank_number)
        message_rank = f"🏆 The rank of the Coinbase app on the App Store is : #️⃣{rank_number_emoji} in Finance."

        sentiment_evaluation = evaluate_sentiment(rank_number)
        change_symbol = compare_ranks(rank_number)

               
        highest_rank, lowest_rank = get_extreme_ranks()
        last_check = f"🔂 Change since last check ({last_rank_date}) : {change_symbol}"
        highest_rank_msg = f"📈 Highest rank: #️⃣{number_to_emoji(highest_rank['rank'])} on {highest_rank['timestamp']}." if highest_rank else "Highest rank data not available."
        lowest_rank_msg = f"📉 Lowest rank: #️⃣{number_to_emoji(lowest_rank['rank'])} on {lowest_rank['timestamp']}." if lowest_rank else "Lowest rank data not available."
        
        save_rank(rank_number)

        await ctx.send(f"{message_rank}\n{sentiment_evaluation}\n{last_check}\n{highest_rank_msg}\n{lowest_rank_msg}")
    else:
        await ctx.send("Rank could not be found.")

bot.run(bot_token)

