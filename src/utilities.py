def number_to_emoji(number):
    digit_to_emoji = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))

def evaluate_sentiment(coinbase_tracker, wallet_tracker):
    # Assuming coinbase_tracker and wallet_tracker are already created and passed to this function

    # Fetch the current ranks from tracker instances
    coinbase_current_rank, _ = coinbase_tracker.get_previous_rank()
    wallet_current_rank, _ = wallet_tracker.get_previous_rank()

    print(f"Debug: Coinbase Rank: {coinbase_current_rank}, Wallet Rank: {wallet_current_rank}")

    # Check if either rank is None
    if None in (coinbase_current_rank, wallet_current_rank):
        print("Debug: One or both ranks are None.")
        return "No data available for sentiment analysis."
    
    try:
        # Ensure ranks are integers for calculation
        coinbase_current_rank = int(coinbase_current_rank)
        wallet_current_rank = int(wallet_current_rank)
        # Calculate weighted average
        weighted_average_rank = (2 * coinbase_current_rank + wallet_current_rank) / 3

        # Evaluate sentiment based on the weighted average
        if weighted_average_rank <= 5:
            return "``🟢 🟢 🟢 Extreme Greed!``"
        elif weighted_average_rank <= 15:
            return "``🟢 🟢 Greed!``"
        elif weighted_average_rank <= 25:
            return "``🟢 Belief``"
        elif weighted_average_rank <= 35:
            return "``🟡 Doubt``"
        elif weighted_average_rank <= 50:
            return "``🟡 🟠 Anxiety``"
        elif weighted_average_rank <= 60:
            return "``🟠 🔴 Fear!``"
        else:
            return "``🔴 🔴 🔴Capitulation!``"

    except TypeError as e:
        print(f"Error in evaluate_sentiment: {e}")
        return "Error processing rank values."

    except ValueError as e:
        print(f"Error converting rank values to integers: {e}")
        return "Error processing rank values."

