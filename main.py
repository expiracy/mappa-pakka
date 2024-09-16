import config
from dbx.dbx_client import DbxClient
from disc.bot import Bot
from helper.task import PeriodicTask
from osu.tools import OsuTools

if __name__ == '__main__':
    config.DATA_FOLDER.mkdir(parents=True, exist_ok=True)
    config.BEATMAPSETS_FOLDER.mkdir(parents=True, exist_ok=True)
    config.MAP_PACKS_FOLDER.mkdir(parents=True, exist_ok=True)

    # Periodic events
    day_1 = 60 * 60 * 24
    periodic_cloud_clean = PeriodicTask(day_1, DbxClient.delete_files_in_folder, (DbxClient.dbx_path,))
    periodic_cloud_clean.start()

    periodic_beatmapset_clean = PeriodicTask(day_1 * 3, OsuTools.clean_beatmapset_folder)
    periodic_beatmapset_clean.start()

    # Run the bot
    bot = Bot()
    bot.run(config.DISCORD_BOT_TOKEN)
