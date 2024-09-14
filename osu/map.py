import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, List

from config import MAP_PACKS_FOLDER, DROPBOX_ACCESS_TOKEN
from helper.log import Logger
from helper.tools import FileTools
from osu.beatmap_extractor import BeatmapExtractor
from osu.clients import OsuClient, DbxClient
from osu.map_id import BeatmapId


class Map:
    """
    Map is a beatmap or a beatmapset
    The osz file is the beatmapset or beatmap file (processed file)
    """

    def __init__(self, map_id, osz_file: Path):
        self.map_id = map_id
        self.osz_file = osz_file

    @classmethod
    def create(cls, map_id, osz_file: Path):
        if isinstance(map_id, BeatmapId):
            Logger.logger.info(f"Extracting beatmap from osz: {map_id}")
            osz_file = BeatmapExtractor(map_id, osz_file).osz_file

        return cls(map_id, osz_file)


class Maps:
    def __init__(self, maps: List[Map]):
        self.maps = maps

    @classmethod
    async def from_map_ids(cls, map_ids: Iterable) -> "Maps":
        valid_map_ids = list(filter(lambda map_id: map_id is not None, map_ids))
        osz_files = await OsuClient.osz_files_from_beatmapset_ids([map_id.beatmapset_id for map_id in valid_map_ids])
        return cls.create_parallel(valid_map_ids, osz_files)

    @classmethod
    def create_parallel(cls, map_ids: Iterable, osz_files: Iterable) -> "Maps":
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(Map.create, map_id, osz_file) for map_id, osz_file in zip(map_ids, osz_files)]
            maps = [future.result() for future in futures]

        return cls(maps)

    def files(self):
        return [m.osz_file for m in self.maps]

    def zip(self):
        map_pack_file = MAP_PACKS_FOLDER.joinpath(f"{uuid.uuid4()}.zip")

        files = self.files()
        FileTools.zip_files(files, to_file=map_pack_file)

        return map_pack_file

    def upload(self):

        DbxClient.init(DROPBOX_ACCESS_TOKEN)

        zf = self.zip()
        dbx_destination = DbxClient.dbx_path + zf.name

        with open(zf, "rb") as f:
            DbxClient.client.files_upload(f.read(), dbx_destination)
            shared_link_metadata = DbxClient.client.sharing_create_shared_link_with_settings(dbx_destination)
            # Temporary file deletion
            files = self.files()
            FileTools.delete_files(files)
            zf.unlink() # am i right in putting this here? It does work but im not sure if this should be here
            return shared_link_metadata.url