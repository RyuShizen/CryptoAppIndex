# CryptoAppIndex

<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/4sLW3yM/Crypto-App-Index-Logo2.png" alt="Crypto-App-Index-Logo2" border="0"></a>
</p>

CryptoAppIndex is a Discord bot designed to provide the current ranking of crypto apps on the App Store directly within your Discord server. By using a simple command, users can quickly get up-to-date information about Crypto's apps popularity, making this bot a must-have for cryptocurrency and finance communities.

## Features

- **Fetch Ranking**: Sends the current ranking of most popular crypto apps (Coinbase, Binance, Crypto.com) on the App Store with simple commands.
- **Automatic Updates**: The bot fetches the most recent data with each command, ensuring the information is always up to date.
- **Daily Monitoring**: Compare the current ranking with that of the day before and indicates the evolution.
- **Market Sentiment**: Analyze the leaderboard to provide market sentiment using a weighted average of crypto apps' rankings. (Extreme Greed, Greed, Optimism, Doubt, etc.).
- **Rank Records**: The bot now tracks the highest and lowest ranks achieved by crypto apps, providing a long-term perspective on their performance in the App Store.

<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/ngMrwKp/Capture.png" alt="Capture" border="0"></a>
</p>

## Installation

To add the CryptoAppIndex to your Discord server, follow these steps:

1. **Create a Discord Application**: Go to the [Discord developer portal](https://discord.com/developers/applications) and create a new application.
2. **Add a Bot to Your Application**: In the "Bot" tab, click "Add Bot".
3. **Invite the Bot to Your Server**: Use the generated invitation URL in the "OAuth2" tab to invite your bot to the server.

or

1. Clone this repository to your server.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Create a `.env` file in the project root and add your `BOT_TOKEN`.
4. Launch the bot with `python bot.py`.

## Usage

After adding CryptoAppIndex to your server, use the following command to get the current ranking of crypto app:

- <code>!coinbase</code> : Get the current ranking of the Coinbase app.
- <code>!cwallet</code> : Get the current ranking of the Coinbase's Wallet app.
- <code>!binance</code> : Get the current ranking of the Binance app.
- <code>!cryptocom</code> : Get the current ranking of the Crypto.com app.

The bot will respond with the current ranking of the app on the App Store.

## License

CryptoAppIndex is distributed under the GNU General Public License v3.0. For more information, see the `LICENSE` file in the project repository.

## Legal Information

This Discord bot is designed solely to retrieve and display the ranking information of specific applications such as Coinbase, Binance, Crypto.com, and Coinbase Wallet from publicly accessible sources. The data provided by this bot is for informational purposes only and should not be interpreted as an endorsement or reflection of the views of the applications concerned or any affiliated platforms, including the App Store. 

Users are advised that all interpretations and actions based on the bot's data are at their own discretion and risk. Importantly, this bot does not provide investment advice, nor should its output be used as a basis for making investment decisions.
