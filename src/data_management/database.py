#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#                     SeedSnake | CryptoAppIndex

#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.

import json
from datetime import datetime
import aiofiles

class AppRankTracker:
    def __init__(self, app_name, file_path):
        self.app_name = app_name
        self.file_path = file_path

    async def save_rank(self, rank_number):
        now = datetime.now()
        current_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

        try:
            async with aiofiles.open(self.file_path, 'r') as f:
                data = await f.read()
                data = json.loads(data)
            last_saved_rank = data.get('last_rank')
        except (FileNotFoundError, json.JSONDecodeError):
            data = {
                'last_rank': None, 
                'date': '',
                'highest_rank': {'rank': None, 'timestamp': ''},
                'lowest_rank': {'rank': None, 'timestamp': ''}
            }
            last_saved_rank = None

        if last_saved_rank != rank_number:
            rank_number = int(rank_number)
            data['last_rank'] = rank_number
            data['date'] = current_datetime

            if data['highest_rank']['rank'] is None or rank_number < data['highest_rank']['rank']:
                data['highest_rank'] = {'rank': rank_number, 'timestamp': current_datetime}
            if data['lowest_rank']['rank'] is None or rank_number > data['lowest_rank']['rank']:
                data['lowest_rank'] = {'rank': rank_number, 'timestamp': current_datetime}

            async with aiofiles.open(self.file_path, 'w') as f:
                await f.write(json.dumps(data, indent=4))
            print("Rank data updated.")
        else:
            print("No need to update rank data; rank unchanged.")

    async def get_extreme_ranks(self):
        """Parcourt l'historique des rangs pour trouver les extrêmes."""
        try:
            async with aiofiles.open(self.file_path, 'r') as file:
                data = await file.read()
                history = json.loads(data)

            highest_rank = {'rank': float('inf'), 'timestamp': None}
            lowest_rank = {'rank': float('-inf'), 'timestamp': None}

            if not isinstance(history, dict):
                raise ValueError("History data is not a dictionary.")

            for year, months in history.items():
                if not isinstance(months, dict):
                    continue

                for month, days in months.items():
                    if not isinstance(days, dict):
                        continue

                    for day, ranks in days.items():
                        for entry in ranks:
                            rank = entry['rank']
                            timestamp = entry['timestamp']
                            if rank < highest_rank['rank']:
                                highest_rank = {'rank': rank, 'timestamp': self.format_timestamp(timestamp)}
                            if rank > lowest_rank['rank']:
                                lowest_rank = {'rank': rank, 'timestamp': self.format_timestamp(timestamp)}

            return highest_rank, lowest_rank

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Failed to read or parse the rank history file: {e}")
            return None, None

    def format_timestamp(self, timestamp):
        """Convertit un timestamp ISO en une date plus lisible."""
        datetime_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        return datetime_obj.strftime('%Y-%m-%d')

    async def get_date_from_json(self):
        try:
            async with aiofiles.open(self.file_path, 'r') as f:
                data = await f.read()
                data = json.loads(data)
            date_value = data.get('date', 'No date found')
            return date_value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading the JSON file: {e}")
            return 'No date found'

    async def get_previous_rank(self):
        try:
            async with aiofiles.open(self.file_path, 'r') as f:
                data = await f.read()
                data = json.loads(data)
            last_rank = data.get('last_rank', None)
            last_date = data.get('date', None)
            return last_rank, last_date
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None

    async def compare_ranks(self, current_rank):
        previous_rank, last_date = await self.get_previous_rank()
        
        if previous_rank is None:
            return "Rank data not available for comparison."

        try:
            current_rank = int(current_rank)
            previous_rank = int(previous_rank)
        except ValueError:
            return "Error processing rank values."

        if current_rank == previous_rank:
            return f"``💤 No Change.``"
        elif current_rank < previous_rank:
            return f"``🔼 Increased by +{previous_rank - current_rank} position(s) since {last_date}``"
        else:
            return f"``🔻 Decreased by -{current_rank - previous_rank} position(s) since {last_date}``"