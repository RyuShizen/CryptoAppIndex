#                     GNU GENERAL PUBLIC LICENSE
#                               Version 3
#                     RyuShizen | CryptoAppIndex

#  Copyright (C) 2024 Free Software Foundation, Inc. <https://fsf.org/>
#  Everyone is permitted to copy and distribute verbatim copies
#  of this license document, but changing it is not allowed.

import json
import os

GUILDS_FILE_PATH = 'data/guilds.json'

def load_guilds():
    """Charge la liste des guildes à partir du fichier JSON."""
    if not os.path.exists(GUILDS_FILE_PATH):
        return []
    with open(GUILDS_FILE_PATH, 'r') as file:
        data = json.load(file)
        return data['guilds']

def save_guilds(guilds):
    """Sauvegarde la liste des guildes dans le fichier JSON."""
    try:
        os.makedirs(os.path.dirname(GUILDS_FILE_PATH), exist_ok=True)
        with open(GUILDS_FILE_PATH, 'w') as file:
            json.dump({"guilds": guilds}, file, indent=4)
        print("Guilds saved successfully.")
    except Exception as e:
        print(f"Failed to save guilds: {e}")

def add_guild(guild_id):
    """Ajoute un guild_id à la liste des guildes et sauvegarde le fichier."""
    guilds = load_guilds()
    if guild_id not in guilds:
        guilds.append(guild_id)
        save_guilds(guilds)

def remove_guild(guild_id):
    """Retire un guild_id de la liste des guildes et sauvegarde le fichier."""
    guilds = load_guilds()
    if guild_id in guilds:
        guilds.remove(guild_id)
        save_guilds(guilds)