"""
Rename this file to config.py and change the values to what you want
"""
from pathlib import Path

ROOT = Path(__file__).parent
BEATMAPSETS_FOLDER = ROOT.joinpath("beatmapsets")
MAP_PACKS_FOLDER = ROOT.joinpath("map_packs")

DATABASE_URL = "postgresql+psycopg2://username:password@localhost/dbname"

DISCORD_BOT_TOKEN: str = ""
OSU_API_CLIENT_ID: int = 0
OSU_API_CLIENT_SECRET: str = ""
