"""
Rename this file to config.py and set the values to match your environment.
"""

from pathlib import Path


"""
Paths
"""
ROOT: Path = Path(__file__).parent
DATA_FOLDER: Path = ROOT.joinpath("data")
BEATMAPSETS_FOLDER: Path = DATA_FOLDER.joinpath("maps")
MAP_PACKS_FOLDER: Path = DATA_FOLDER.joinpath("map_packs")
LOG_FOLDER: Path = DATA_FOLDER.joinpath("logs")


"""
PERSISTENCE
"""
DATABASE_URL: str = "postgresql+psycopg2://james:james@localhost/dbname"


"""
DISCORD
"""
DISCORD_BOT_TOKEN: str = ""


"""
OSU
"""
OSU_API_CLIENT_ID: int = 0
OSU_API_CLIENT_SECRET: str = ""


"""
DROPBOX
"""
DROPBOX_ACCESS_TOKEN: str = ""
DROPBOX_APP_KEY: str = ""
DROPBOX_APP_SECRET: str = ""
DROPBOX_REFRESH_TOKEN: str = ""
