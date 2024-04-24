# CryptoAppIndex Bot

<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/cD9NhBY/coinbase-rank-logo250.png" alt="coinbase-rank-logo250" border="0"></a>
</p>

CryptoAppIndex is a Discord bot designed to provide the current ranking of the Coinbase app wallet (more apps to come) on the App Store directly within your Discord server. By using a simple command, users can quickly get up-to-date information about Coinbase's popularity, making this bot a must-have for cryptocurrency and finance communities.

## Features

- **Fetch Ranking**: Sends the current ranking of both the Coinbase apps and Coinbase Wallet on the App Store with simple commands.
- **Automatic Updates**: The bot fetches the most recent data with each command, ensuring the information is always up to date.
- **Daily Monitoring**: Compare the current ranking with that of the day before and indicates the evolution.
- **Market Sentiment**: Analyze the leaderboard to provide market sentiment using a weighted average of both apps' rankings. (Extreme Greed, Greed, Belief, etc.).
- **Rank Records**: The bot now tracks the highest and lowest ranks achieved by both the Coinbase and Wallet apps, providing a long-term perspective on their performance in the App Store.

<p align="center">
<a href="https://imgbb.com/"><img src="https://i.ibb.co/wKfhVxR/Capture.png" alt="Capture" border="0"></a>
</p>

## Installation

To add the Coinbase Rank Bot to your Discord server, follow these steps:

1. **Create a Discord Application**: Go to the [Discord developer portal](https://discord.com/developers/applications) and create a new application.
2. **Add a Bot to Your Application**: In the "Bot" tab, click "Add Bot".
3. **Invite the Bot to Your Server**: Use the generated invitation URL in the "OAuth2" tab to invite your bot to the server.

or

1. Clone this repository to your server.
2. Install the dependencies by running `pip install -r requirements.txt`.
3. Create a `.env` file in the project root and add your `BOT_TOKEN`.
4. Launch the bot with `python bot.py`.

## Usage

After adding the Coinbase Rank Bot to your server, use the following command to get the current ranking of the Coinbase app:

- <code>!coinbase</code> : Get the current ranking of the Coinbase app.
- <code>!cwallet</code> : Get the current ranking of the Coinbase Wallet app.

The bot will respond with the current ranking of the app on the App Store.

## Contribution

If you wish to contribute to the development of the Coinbase Rank Bot, please follow these steps:

1. **Fork the Repository**: Create a fork of the project on GitHub.
2. **Clone Your Fork**: Work on your local machine to make changes.
3. **Submit a Pull Request**: Submit your improvements for review.

For any questions or suggestions, feel free to open an issue in the project's GitHub repository.

## License

The Coinbase Rank Bot is distributed under the MIT License. For more information, see the `LICENSE` file in the project repository.


