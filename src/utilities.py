#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#                     SeedSnake | CryptoAppIndex

#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.

from api.apps import current_rank_binance, current_rank_coinbase, current_rank_cryptodotcom, current_rank_wallet

def number_to_emoji(number):
    digit_to_emoji = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    try:
        return ''.join(digit_to_emoji[digit] for digit in str(number) if digit.isdigit())
    except KeyError as e:
        print(f"Non-digit character encountered: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

async def evaluate_sentiment():
    coinbase_current_rank = await current_rank_coinbase()
    wallet_current_rank = await current_rank_wallet()
    binance_current_rank = await current_rank_binance()
    cryptodotcom_current_rank = await current_rank_cryptodotcom()

    if None in (coinbase_current_rank, wallet_current_rank, binance_current_rank, cryptodotcom_current_rank):
        print("Debug: One or both ranks are None.")
        return "No data available for sentiment analysis.", None

    try:
        coinbase_current_rank = int(coinbase_current_rank)
        wallet_current_rank = int(wallet_current_rank)
        binance_current_rank = int(binance_current_rank)
        cryptodotcom_current_rank = int(cryptodotcom_current_rank)
        
        weighted_average_rank = 100 - (5 * (coinbase_current_rank + cryptodotcom_current_rank) + 2.5 * binance_current_rank + wallet_current_rank) / 13.5
        
        sentiment, image_file = await evaluate_based_on_weighted_average(weighted_average_rank)

        return sentiment, image_file

    except TypeError as e:
        print(f"Error in evaluate_sentiment: {e}")
        return "Error processing rank values.", None

    except ValueError as e:
        print(f"Error converting rank values to integers: {e}")
        return "Error processing rank values.", None

async def evaluate_based_on_weighted_average(weighted_average_rank):
    if weighted_average_rank >= 90:
        sentiment = "🟢🟢🟢 Extreme Greed!"
    elif weighted_average_rank >= 80:
        sentiment = "🟢🟢 Greed!"
    elif weighted_average_rank >= 75:
        sentiment = "🟢 Optimism"
    elif weighted_average_rank >= 70:
        sentiment = "🟡 Doubt"
    elif weighted_average_rank >= 65:
        sentiment = "🟠 Anxiety"
    elif weighted_average_rank >= 50:
        sentiment = "🔴🔴 Fear!"
    else:
        sentiment = "🔴🔴🔴 Capitulation!"

    sentiment_images = {
        "🟢🟢🟢 Extreme Greed!": "extreme_greed.png",
        "🟢🟢 Greed!": "greed.png",
        "🟢 Optimism": "optimism.png",
        "🟡 Doubt": "doubt.png",
        "🟠 Anxiety": "anxiety.png",
        "🔴🔴 Fear!": "fear.png",
        "🔴🔴🔴 Capitulation!": "capitulation.png"
    }
    
    image_file = sentiment_images.get(sentiment)
    return sentiment, image_file

async def weighted_average_sentiment_calculation():
    rank_number_coinbase = int(await current_rank_coinbase())
    rank_number_binance = int(await current_rank_binance())
    rank_number_wallet = int(await current_rank_wallet())
    rank_number_cryptodotcom = int(await current_rank_cryptodotcom())

    weighted_average_rank = (5 * (rank_number_coinbase + rank_number_cryptodotcom) + 2.5 * rank_number_binance + rank_number_wallet) / 13.5

    return 100 - round(weighted_average_rank)