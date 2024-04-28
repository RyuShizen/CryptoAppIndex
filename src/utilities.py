from api.apps import current_rank_binance, current_rank_coinbase, current_rank_cryptodotcom, current_rank_wallet

def number_to_emoji(number):
    digit_to_emoji = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))

def evaluate_sentiment(coinbase_tracker, wallet_tracker, binance_tracker, cryptodotcom_tracker):
    # Assuming coinbase_tracker and other apps are already created and passed to this function

    # Fetch the current ranks from tracker instances
    coinbase_current_rank, _ = coinbase_tracker.get_previous_rank()
    wallet_current_rank, _ = wallet_tracker.get_previous_rank()
    binance_current_rank, _ = binance_tracker.get_previous_rank()
    cryptodotcom_current_rank, _ = cryptodotcom_tracker.get_previous_rank()

    print(f"Debug: Coinbase Rank: {coinbase_current_rank}, Wallet Rank: {wallet_current_rank}, Binance Rank: {binance_current_rank}, Crypto.com Rank: {cryptodotcom_current_rank}")

    # Check if either rank is None
    if None in (coinbase_current_rank, wallet_current_rank, binance_current_rank, cryptodotcom_current_rank):
        print("Debug: One or both ranks are None.")
        return "No data available for sentiment analysis."
    
    try:
        # Ensure ranks are integers for calculation
        coinbase_current_rank = int(coinbase_current_rank)
        wallet_current_rank = int(wallet_current_rank)
        binance_current_rank = int(binance_current_rank)
        cryptodotcom_current_rank = int(cryptodotcom_current_rank)
        # Calculate weighted average
        weighted_average_rank = (5 * (coinbase_current_rank + cryptodotcom_current_rank) + 2.5 * binance_current_rank + wallet_current_rank) / 13.5
        
        print(f"Debug: Weighted Average Rank Result: {100 - round(weighted_average_rank)}.")

        # Evaluate sentiment based on the weighted average
        if weighted_average_rank < 10:
            sentiment = "🟢🟢🟢 Extreme Greed!"
        elif weighted_average_rank < 20:
            sentiment = "🟢🟢 Greed!"
        elif weighted_average_rank < 25:
            sentiment = "🟢 Optimism"
        elif weighted_average_rank < 30:
            sentiment = "🟡 Doubt"
        elif weighted_average_rank < 35:
            sentiment = "🟠 Anxiety"
        elif weighted_average_rank < 50:
            sentiment = "🔴🔴 Fear!"
        else:
            sentiment = "🔴🔴🔴 Capitulation!"

        # Ajoutez une correspondance sentiment-image
        sentiment_images = {
            "🟢🟢🟢 Extreme Greed!": "extreme_greed.png",
            "🟢🟢 Greed!": "greed.png",
            "🟢 Optimism": "optimism.png",
            "🟡 Doubt": "doubt.png",
            "🟠 Anxiety": "anxiety.png",
            "🔴🔴 Fear!": "fear.png",
            "🔴🔴🔴 Capitulation!": "capitulation.png"
        }

        # Choisissez l'image basée sur le sentiment calculé
        image_file = sentiment_images.get(sentiment)

        return sentiment, image_file
    
    except TypeError as e:
        print(f"Error in evaluate_sentiment: {e}")
        return "Error processing rank values."

    except ValueError as e:
        print(f"Error converting rank values to integers: {e}")
        return "Error processing rank values."

def weighted_average_sentiment_calculation():

    rank_number_coinbase = int(current_rank_coinbase())
    rank_number_binance = int(current_rank_binance())
    rank_number_wallet = int(current_rank_wallet())
    rank_number_cryptocom = int(current_rank_cryptodotcom())

    weighted_average_rank = (5 * (rank_number_coinbase + rank_number_cryptocom) + 2.5 * rank_number_binance + rank_number_wallet) / 13.5

    return 100 - round(weighted_average_rank)
