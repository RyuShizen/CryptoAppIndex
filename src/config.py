import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN_TEST')
discord_user_id = os.getenv("DISCORD_USER_ID")