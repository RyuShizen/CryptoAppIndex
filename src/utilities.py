from data_management.database import AppRankTracker

def number_to_emoji(number):
    digit_to_emoji = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    return ''.join(digit_to_emoji[digit] for digit in str(number))

def evaluate_sentiment(coinbase_tracker, wallet_tracker):
    # Fetch the current ranks from tracker instances
    coinbase_current_rank, _ = coinbase_tracker.get_previous_rank()
    wallet_current_rank, _ = wallet_tracker.get_previous_rank()

    # Check if either rank is None
    if coinbase_current_rank is None or wallet_current_rank is None:
        return "No data available for sentiment analysis."
    
    try:
        # Ensure ranks are integers for calculation
        coinbase_current_rank = int(coinbase_current_rank)
        wallet_current_rank = int(wallet_current_rank)
        # Calculate weighted average
        weighted_average_rank = (2 * coinbase_current_rank + wallet_current_rank) / 3

        # Evaluate sentiment based on the weighted average
        if weighted_average_rank <= 10:
            return "🟢 Greed!"
        elif weighted_average_rank <= 50:
            return "🟡 Neutral."
        else:
            return "🔴 Fear."
    except TypeError:
        return "Error processing rank values."


