import config
from helper.log import Logger


class OsuTools:
    @staticmethod
    def clean_beatmapset_folder():
        try:
            beatmapset_files = config.BEATMAPSETS_FOLDER.glob("*")
            for file in beatmapset_files:
                Logger.mappa_pakka.info(f"Cleaning beatmapset folder: {file}")
                file.unlink()
        except Exception as e:
            Logger.mappa_pakka.error(f"Failed to clean beatmapset folder: {e}")
