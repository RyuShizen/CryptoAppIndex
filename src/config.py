#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007
#                     SeedSnake | CryptoAppIndex

#  Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN_TEST')
discord_user_id = os.getenv("DISCORD_USER_ID")