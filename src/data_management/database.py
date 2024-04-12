import json
from datetime import datetime

class AppRankTracker:
    def __init__(self, app_name, file_path):
        self.app_name = app_name
        self.file_path = file_path

    def save_rank(self, rank_number):
        now = datetime.now()
        current_datetime_hour = now.strftime('%Y-%m-%d %H')
        
        try:
            with open(self.file_path, 'r') as f:
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

            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=4)

    def get_extreme_ranks(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            highest_rank = data.get('highest_rank', {})
            lowest_rank = data.get('lowest_rank', {})
            return highest_rank, lowest_rank
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None

    def get_date_from_json(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            date_value = data.get('date', 'No date found')
            return date_value
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading the JSON file: {e}")
            return 'No date found'

    def get_previous_rank(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            last_rank = data.get('last_rank', None)
            last_date = data.get('date', None)
            return last_rank, last_date
        except (FileNotFoundError, json.JSONDecodeError):
            return None, None

    def compare_ranks(self, current_rank):
        previous_rank, last_date = self.get_previous_rank()
        if previous_rank is None:
            return "Rank data not available for comparison."

        try:
            current_rank = int(current_rank)
            previous_rank = int(previous_rank)
        except ValueError:
            return "Error processing rank values."

        if current_rank == previous_rank:
            return f"💤 (No Change)."
        elif current_rank < previous_rank:
            return f"🔼 Increased by +{previous_rank - current_rank} position(s) since {last_date}"
        else:
            return f"🔻 Decreased by -{current_rank - previous_rank} position(s) since {last_date}"
