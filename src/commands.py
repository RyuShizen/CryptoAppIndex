#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#                     SeedSnake | CryptoAppIndex

#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.

import discord
import json
import os
from datetime import datetime, timedelta
from discord import app_commands, Interaction, File, Embed, Colour
from discord.ext import commands
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

from api.apps import current_rank_coinbase, current_rank_wallet, current_rank_binance, current_rank_cryptodotcom, get_bitcoin_price_usd
from utilities import number_to_emoji, evaluate_sentiment, weighted_average_sentiment_calculation
from data_management.database import AppRankTracker
from tracker import RankTracker
from data_management.guilds import load_guilds
from config import discord_user_id

coinbase_tracker = AppRankTracker('Coinbase', 'data/rank_data_coinbase.json')
wallet_tracker = AppRankTracker('Wallet', 'data/rank_data_wallet.json')
binance_tracker = AppRankTracker('Binance', 'data/rank_data_binance.json')
cryptodotcom_tracker = AppRankTracker('Crypto.com', 'data/rank_data_cryptodotcom.json')
app_rank_tracker = AppRankTracker(app_name="my_app", file_path="data/last_execution_time.json")

ath_coinbase_tracker = AppRankTracker('coinbase', 'data/coinbase_rank_history.json')
ath_wallet_tracker = AppRankTracker('wallet', 'data/wallet_rank_history.json')
ath_binance_tracker = AppRankTracker('binance', 'data/binance_rank_history.json')
ath_cryptodotcom_tracker = AppRankTracker('cryptocom', 'data/cryptocom_rank_history.json')

async def limit_command(interaction: Interaction):
    user_id = str(interaction.user.id)
    last_execution_times = await app_rank_tracker.read_last_execution_times()
    now = datetime.now()

    if user_id in last_execution_times:
        last_time = datetime.fromisoformat(last_execution_times[user_id])
        if now - last_time < timedelta(minutes=1):
            await interaction.response.send_message("❗ You can call command only once per minute. ❗", ephemeral=True)
            return False

    last_execution_times[user_id] = now.isoformat()
    await app_rank_tracker.write_last_execution_times(last_execution_times)

    return True

async def setup_commands(bot):

    async def send_error_message_set_alert(interaction: discord.Interaction, additional_info=""):
        embed = discord.Embed(
            title="❌ Missing argument",
            description="One or more arguments are missing.",
            color=discord.Color.red()
        )
        embed.add_field(name="Format Correct", value="`/alert <app-name> <operator> <rank>`")
        if additional_info:
            embed.add_field(name="Error", value=additional_info)
        embed.add_field(name="Example", value="`/alert coinbase > 10`")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def send_error_message_remove_alert(interaction: discord.Interaction, additional_info=""):
        embed = discord.Embed(
            title="❌ Missing argument",
            description="One or more arguments are missing.",
            color=discord.Color.red()
        )
        embed.add_field(name="Format Correct", value="`/remove_alert <app-name>`")
        if additional_info:
            embed.add_field(name="Error", value=additional_info)
        embed.add_field(name="Example", value="`/remove_alert coinbase`")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else discord.Embed.Empty)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="coinbase", description="Get the current rank of the Coinbase app")
    async def coinbase_command(interaction: Interaction):
        if not await limit_command(interaction):
            return
        
        now = datetime.now()
        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_coinbase = await current_rank_coinbase()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await coinbase_tracker.compare_ranks(rank_number_coinbase)
        highest_rank, lowest_rank = await ath_coinbase_tracker.get_extreme_ranks()

        embed = Embed(title="Coinbase Statistics", description="Real-time tracking and analysis of the Coinbase app ranking.", color=0x0052ff)
        file_thumb = File("assets/coinbase-coin-seeklogo.png", filename="coinbase_logo.png")
        embed.set_thumbnail(url="attachment://coinbase_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_coinbase)} ``in Finance on {current_datetime_hour}``", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} ``on {highest_rank['timestamp']}``", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} ``on {lowest_rank['timestamp']}``", inline=True)
        embed.add_field(name="🚥 Current Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await coinbase_tracker.save_rank(rank_number_coinbase)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="cwallet", description="Get the current rank of the Coinbase Wallet app")
    async def cwallet_command(interaction: Interaction):
        if not await limit_command(interaction):
            return
        
        now = datetime.now()

        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_wallet = await current_rank_wallet()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await wallet_tracker.compare_ranks(rank_number_wallet)
        highest_rank, lowest_rank = await ath_wallet_tracker.get_extreme_ranks()

        embed = Embed(title="Coinbase's Wallet Statistics", description="Real-time tracking and analysis of the Coinbase's Wallet app ranking.", color=0x0052ff)
        file_thumb = File("assets/coinbase-wallet-seeklogo.png", filename="coinbase_wallet_logo.png")
        embed.set_thumbnail(url="attachment://coinbase_wallet_logo.png")

        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_wallet)} ``in Finance on {current_datetime_hour}``", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} ``on {highest_rank['timestamp']}``", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} ``on {lowest_rank['timestamp']}``", inline=True)

        embed.add_field(name="🚥 Current Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")

        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await wallet_tracker.save_rank(rank_number_wallet)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="binance", description="Get the current rank of the Binance app")
    async def binance_command(interaction: Interaction):
        if not await limit_command(interaction):
            return
        
        now = datetime.now()
        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_binance = await current_rank_binance()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await binance_tracker.compare_ranks(rank_number_binance)
        highest_rank, lowest_rank = await ath_cryptodotcom_tracker.get_extreme_ranks()

        embed = Embed(title="Binance Statistics", description="Real-time tracking and analysis of the Binance app ranking.", color=0xf3ba2f)
        file_thumb = File("assets/binance-smart-chain-bsc-seeklogo.png", filename="binance_logo.png")
        embed.set_thumbnail(url="attachment://binance_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_binance)} ``in Finance on {current_datetime_hour}``", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} ``on {highest_rank['timestamp']}``", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} ``on {lowest_rank['timestamp']}``", inline=True)
        embed.add_field(name="🚥 Current Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await binance_tracker.save_rank(rank_number_binance)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="cryptocom", description="Get the current rank of the Crypto.com app")
    async def cryptocom_command(interaction: Interaction):
        if not await limit_command(interaction):
            return
        
        now = datetime.now()
        average_sentiment_calculation = await weighted_average_sentiment_calculation()
        rank_number_cryptodotcom = await current_rank_cryptodotcom()
        current_datetime_hour = now.strftime('%Y-%m-%d at %H:%M:%S')

        sentiment_text, sentiment_image_filename = await evaluate_sentiment()
        change_symbol = await cryptodotcom_tracker.compare_ranks(rank_number_cryptodotcom)
        highest_rank, lowest_rank = await ath_cryptodotcom_tracker.get_extreme_ranks()

        embed = Embed(title="Crypto.com Statistics", description="Real-time tracking and analysis of the Crypto.com app ranking.", color=0x1c64b0)
        file_thumb = File("assets/crypto-com-seeklogo.png", filename="cryptodotcom_logo.png")
        embed.set_thumbnail(url="attachment://cryptodotcom_logo.png")
        embed.add_field(name="🏆 Current Rank", value=f"#️⃣{number_to_emoji(rank_number_cryptodotcom)} ``in Finance on {current_datetime_hour}``", inline=False)
        embed.add_field(name="🔂 Recent Positional Change", value=change_symbol, inline=False)
        if highest_rank:
            embed.add_field(name="📈 Peak Rank Achieved (ATH)", value=f"#️⃣{number_to_emoji(highest_rank['rank'])} ``on {highest_rank['timestamp']}``", inline=True)
        if lowest_rank:
            embed.add_field(name="📉 Recent Lowest Rank (ATL)", value=f"#️⃣{number_to_emoji(lowest_rank['rank'])} ``on {lowest_rank['timestamp']}``", inline=True)
        embed.add_field(name="🚥 Current Market Sentiment", value=f"Score: ``{average_sentiment_calculation}``\nFeeling: ``{sentiment_text}``", inline=False)
        file_sentiment = File(f"assets/{sentiment_image_filename}", filename=sentiment_image_filename)
        embed.set_image(url=f"attachment://{sentiment_image_filename}")
        avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
        embed.set_footer(text=f"Requested by {interaction.user.display_name}, {current_datetime_hour}.", icon_url=avatar_url if avatar_url else None)

        await cryptodotcom_tracker.save_rank(rank_number_cryptodotcom)
        await interaction.response.send_message(files=[file_thumb, file_sentiment], embed=embed)

    @bot.tree.command(name="set_alert", description="Set an alert to be notified when a specific crypto app reaches a designated rank.")
    @app_commands.describe(
        operator="The comparison operator for the alert (e.g., >, <, >=, <=)",
        rank="The rank threshold for the alert"
    )
    @app_commands.choices(
        app_name=[
            app_commands.Choice(name="Coinbase", value="coinbase"),
            app_commands.Choice(name="Coinbase wallet", value="cwallet"),
            app_commands.Choice(name="Crypto.com", value="cryptocom"),
            app_commands.Choice(name="Binance", value="binance")
        ],
        operator=[
            app_commands.Choice(name="greater than", value=">"),
            app_commands.Choice(name="less than", value="<"),
            app_commands.Choice(name="greater than or equal to", value=">="),
            app_commands.Choice(name="less than or equal to", value="<=")
        ]
    )
    async def set_alert_command(interaction: Interaction, app_name: str, operator: str, rank: int):
        alert_data = {
            'user_id': interaction.user.id,
            'app_name': app_name.lower(),
            'operator': operator,
            'rank': rank
        }

        os.makedirs('data', exist_ok=True)

        try:
            alerts = []
            if os.path.exists('data/alerts.json'):
                with open('data/alerts.json', 'r') as f:
                    alerts = json.load(f)
            
            for existing_alert in alerts:
                if existing_alert['user_id'] == interaction.user.id:
                    embed = Embed(description=f"❌ You have reached your maximum number of alerts. See your current alerts with the ``/myalerts`` command.", color=0xff0000)
                    avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            
            alerts.append(alert_data)
            with open('data/alerts.json', 'w') as f:
                json.dump(alerts, f, indent=4)

            embed = Embed(description=f"✅🔔 Alert set for ``{app_name}`` when rank ``{operator} {rank}``.", color=0x00ff00)
            avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
            await interaction.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            print(f"Failed to set or check alerts due to an error: {e}")
            await interaction.response.send_message("🚨 Failed to set alert due to an internal error.", ephemeral=True)

    @bot.tree.command(name="set_notification", description="Receive daily or weekly updates on the position of a specific crypto app on the App Store.")
    @app_commands.describe(
    interval = "The interval to send notifications for your specific crypto app (daily, weekly)",
    hour = "The hour of the day to receive the notification (6 AM, 12 PM, 6 PM, 10 PM)"
    )
    @app_commands.choices(
        app_name=[
            app_commands.Choice(name="Coinbase", value="coinbase"),
            app_commands.Choice(name="Coinbase wallet", value="cwallet"),
            app_commands.Choice(name="Crypto.com", value="cryptocom"),
            app_commands.Choice(name="Binance", value="binance")
        ],
        interval=[
            app_commands.Choice(name="daily", value="daily"),
            app_commands.Choice(name="weekly", value="weekly"),
        ],
        hour=[
            app_commands.Choice(name="6 AM", value="6:00"),
            app_commands.Choice(name="12 PM", value="12:00"),
            app_commands.Choice(name="6 PM", value="18:00"),
            app_commands.Choice(name="10 PM", value="22:00")
        ]
    )
    async def set_notif_command(interaction: Interaction, app_name: str, interval: str, hour: str):
        now = datetime.now()
        current_week = now.strftime('%U')
        notif_data = {
            'user_id': interaction.user.id,
            'app_name': app_name.lower(),
            'interval': interval,
            'hour': hour,
            'week': current_week,
            'last_sent_week': None,
            'last_sent_day': None
        }

        os.makedirs('data', exist_ok=True)

        try:
            notifs = []
            if os.path.exists('data/notifs.json'):
                with open('data/notifs.json', 'r') as f:
                    notifs = json.load(f)
            
            for existing_notif in notifs:
                if existing_notif['user_id'] == interaction.user.id:

                    embed = Embed(description=f"❌ You have reached your maximum number of notifications. See your current notifications with the ``/myalerts`` command.", color=0xff0000)
                    avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            
            notifs.append(notif_data)
            with open('data/notifs.json', 'w') as f:
                json.dump(notifs, f, indent=4)

            embed = Embed(description=f"✅📆🔔``{interval.capitalize()}`` notification set for ``{app_name}`` rank on the App Store at ``{hour}``.", color=0x00ff00)
            avatar_url = interaction.user.avatar.url if interaction.user.avatar else None
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=avatar_url if avatar_url else None)
            await interaction.response.send_message(embed=embed, ephemeral=False)

        except Exception as e:
            print(f"Failed to set or check notifs due to an error: {e}")
            await interaction.response.send_message("🚨 Failed to set notif due to an internal error.", ephemeral=True)

    @bot.tree.command(name="remove_alert", description="Remove an existing alert for a specific app")
    @app_commands.describe(app_name="The name of the application to remove the alert for")
    async def remove_alert_command(interaction: Interaction, app_name: str):
        if app_name is None:
            await send_error_message_remove_alert(interaction)
            return

        user_id = interaction.user.id
        alert_file_path = 'data/alerts.json'

        try:
            with open(alert_file_path, 'r+') as file:
                alerts = json.load(file)
                new_alerts = [alert for alert in alerts if not (alert['user_id'] == user_id and alert['app_name'].lower() == app_name.lower())]

                if len(alerts) == len(new_alerts):
                    embed = Embed(description=f"🙅‍♂️ No alert found for `{app_name.capitalize()}` that belongs to you.", color=Colour.red())
                else:
                    file.seek(0)
                    json.dump(new_alerts, file, indent=4)
                    file.truncate()
                    embed = Embed(description=f"🚮 Alert for `{app_name.capitalize()}` has been successfully removed.", color=Colour.green())

                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except FileNotFoundError:
            embed = Embed(description="🚨 Alert data file not found.", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except json.JSONDecodeError:
            embed = Embed(description="🚨 Error reading the alert data.", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 Failed to remove the alert due to an error: {e}", color=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="myalerts", description="Display your active alerts and notifications")
    async def myalerts_command(interaction: Interaction):
        user_id = interaction.user.id
        alert_file_path = 'data/alerts.json'
        notif_file_path = 'data/notifs.json'

        try:
            with open(alert_file_path, 'r') as file_alerts:
                alerts = json.load(file_alerts)
                user_alerts = [alert for alert in alerts if int(alert['user_id']) == user_id]
            with open(notif_file_path, 'r') as file_notifs:
                notifs = json.load(file_notifs)
                user_notifs = [notif for notif in notifs if int(notif['user_id']) == user_id]

            if not user_alerts and not user_notifs:
                embed = Embed(description="🤷‍♂️ You have no active alerts nor notifications.", color=Colour.blue())
            else:
                embed = Embed(title="🔂🔔 Your Active Alerts & Notifications.", description="", color=Colour.green())
                for alert in user_alerts: 
                    embed.add_field(name=f"✅📢 {alert['app_name'].title()} alert(s)",
                                    value=f"``Trigger: {alert['operator']} {alert['rank']}.``",
                                    inline=False)
                for notif in user_notifs: 
                    embed.add_field(name=f"✅📆 {notif['app_name'].title()} notification(s)",
                                    value=f"``Frequency: {notif['interval']} at {notif['hour']}.``",
                                    inline=False)

            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except FileNotFoundError:
            embed = Embed(description="🚨 Alert data file not found.", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except json.JSONDecodeError:
            embed = Embed(description="🚨 Error reading the alert data.", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 An error occurred while retrieving your alerts: {e}", color=Colour.red())
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="remove_all_alerts", description="Remove all your set alerts")
    async def remove_all_alerts_command(interaction: Interaction):
        user_id = interaction.user.id
        try:
            if os.path.exists('data/alerts.json'):
                with open('data/alerts.json', 'r') as file:
                    alerts = json.load(file)
                
                user_alerts = [alert for alert in alerts if alert['user_id'] == user_id]

                if not user_alerts:
                    embed = Embed(description="🤷‍♂️ You have no alerts to remove.", color=Colour.blue())
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                alerts = [alert for alert in alerts if alert['user_id'] != user_id]

                with open('data/alerts.json', 'w') as file:
                    json.dump(alerts, file, indent=4)
                
                embed = Embed(title="🚮✅ Alerts Removed", description="All your alerts have been successfully removed.", color=0x00ff00)
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = Embed(description="🤷‍♂️ No alert file found or no alerts set.", color=Colour.blue())
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except json.JSONDecodeError as e:
            embed = Embed(description=f"🚨 Error reading the alert data: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 Failed to remove alerts due to an error: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="remove_all_notifications", description="Remove all your set notifications")
    async def remove_all_notifications_command(interaction: Interaction):
        user_id = interaction.user.id
        try:
            if os.path.exists('data/notifs.json'):
                with open('data/notifs.json', 'r') as file:
                    notifs = json.load(file)
                
                user_notifs = [notif for notif in notifs if notif['user_id'] == user_id]

                if not user_notifs:
                    embed = Embed(description="🤷‍♂️ You have no notifications to remove.", color=Colour.blue())
                    embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                notifs = [notif for notif in notifs if notif['user_id'] != user_id]

                with open('data/notifs.json', 'w') as file:
                    json.dump(notifs, file, indent=4)
                
                embed = Embed(title="🚮✅ Notifications Removed", description="All your notifications have been successfully removed.", color=0x00ff00)
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = Embed(description="🤷‍♂️ No notification file found or no notif(s) set.", color=Colour.blue())
                embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
                await interaction.response.send_message(embed=embed, ephemeral=True)

        except json.JSONDecodeError as e:
            embed = Embed(description=f"🚨 Error reading the notif data: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = Embed(description=f"🚨 Failed to remove notifs due to an error: {str(e)}", color=0xff0000)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @bot.tree.command(name="all_ranks", description="Display ranks and Data History of all crypto apps at once")
    async def all_ranks_command(interaction: Interaction):
        if not await limit_command(interaction):
            return
        
        rank_tracker = RankTracker(bot)

        bitcoin_price = await get_bitcoin_price_usd()  
        bitcoin_emoji_id = "1234500592559194164"
        bitcoin_emoji = f"<:bitcoin:{bitcoin_emoji_id}>"
        bitcoin_price_text = f"``Current Bitcoin Price: 💲{bitcoin_price:,.2f} USD``" if bitcoin_price != "Unavailable" else f"{bitcoin_emoji} Bitcoin Price: Unavailable"

        embed = Embed(title="Crypto App Ranks", description="Current and historical ranks of major crypto apps on the App Store in Finance category.", color=0x4ba1da)
        file_thumb = File("assets/Logo_App_Store.png", filename="app_store_logo.png")
        embed.set_thumbnail(url="attachment://app_store_logo.png")
        embed.add_field(name=f"{bitcoin_emoji} Bitcoin Price", value=bitcoin_price_text, inline=False)

        apps = ["coinbase", "wallet", "binance", "cryptocom"]
        emoji_ids = {
            "coinbase": "<:coinbase_icon:1234492789967032330>",
            "wallet": "<:wallet_icon:1234492792320036925>",
            "binance": "<:binance_icon:1234492788616331295>",
            "cryptocom": "<:cryptocom_icon:1234492791355080874>"
        }

        logging.debug(f"Awaiting fetch_all_ranks")
        current_ranks = await rank_tracker.fetch_all_ranks()

        for idx, app in enumerate(apps):
            logging.debug(f"Awaiting get_historical_rank for {app} yesterday")
            yesterday_rank = await rank_tracker.get_historical_rank(app, days_back=1)
            last_week_rank = await rank_tracker.get_historical_rank(app, days_back=7)
            last_month_rank = await rank_tracker.get_historical_rank(app, months_back=1)

            current_rank = current_ranks[idx] if current_ranks[idx] is not None else "Unavailable"

            change_text = "No data"
            if isinstance(current_rank, int) and isinstance(yesterday_rank, int):
                if current_rank < yesterday_rank:
                    change_icon = " 🔼 +"
                    change = yesterday_rank - current_rank
                elif current_rank > yesterday_rank:
                    change_icon = " 🔻 -"
                    change = current_rank - yesterday_rank
                else:
                    change_icon = ""
                    change = ""
                change_text = f"{change_icon}{change}" if change_icon else " 💤 No change "
            else:
                change_text = "Data unavailable"

            embed.add_field(
                name=f"{emoji_ids[app]} {app.capitalize()} Rank",
                value=f"|``Current``: #️⃣{number_to_emoji(current_rank)} ({change_text} ) \n-| ``Yesterday``: #️⃣{number_to_emoji(yesterday_rank)} \n--| ``Last Week``: #️⃣{number_to_emoji(last_week_rank)} \n---| ``Last Month``: #️⃣{number_to_emoji(last_month_rank)}",
                inline=False
            )

        await interaction.response.send_message(files=[file_thumb], embed=embed)

    @bot.tree.command(name="maintenance", description="Toggle maintenance mode for the bot.")
    @app_commands.describe(mode="Enter 'on' to start maintenance or 'off' to end it.", reason="Reason for maintenance")
    @app_commands.choices(mode=[
        app_commands.Choice(name='on', value='on'),
        app_commands.Choice(name='off', value='off')
    ])
    async def maintenance_command(interaction: discord.Interaction, mode: str, reason: str = "No specific reason provided."):
        """Handle the maintenance mode command."""
        if interaction.user.id == int(discord_user_id):
            if mode == 'on':
                message = f"🔧 The bot is currently under maintenance. We will come back soon ! \n\n **Issue** : {reason}"
            else:
                message = f"✅ Maintenance is complete. Thank you for your patience ! \n\n **Changelog** : {reason}"
            
            embed = discord.Embed(title="📢 Maintenance Notice!", description=message, color=0xFF5733 if mode.lower() == "on" else 0x00ff00)
            embed.set_footer(text="Thank you for your patience.")
            
            await notify_all_servers(embed)
            await interaction.response.send_message(f"Maintenance mode set to {mode}.", ephemeral=True)
        else:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)

    async def notify_all_servers(embed):
        """Send a notification message to all guilds."""
        guild_ids = load_guilds()
        for guild_id in guild_ids:
            guild = bot.get_guild(guild_id)
            if guild:
                target_channel = guild.system_channel
                if not target_channel:
                    for channel in guild.text_channels:
                        if channel.permissions_for(guild.me).send_messages:
                            target_channel = channel
                            break
                if target_channel:
                    await target_channel.send(embed=embed)