import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, List

from config import MAP_PACKS_FOLDER
from helper.log import Logger
from helper.tools import FileTools
from osu.beatmap_extractor import BeatmapExtractor
from osu.map_id import BeatmapId
from osu.osu_client import OsuClient


class Map:
    """
    Map is a beatmap or a beatmapset
    The osz file is the beatmapset or beatmap file (processed file)
    """

    def __init__(self, map_id, osz_file: Path, temporary: bool = False):
        self.map_id = map_id
        self.osz_file = osz_file
        self.temporary = temporary

    @classmethod
    def create(cls, map_id, osz_file: Path):
        if isinstance(map_id, BeatmapId):
            Logger.mappa_pakka.info(f"Extracting beatmap from osz: {map_id}")
            with BeatmapExtractor(map_id, osz_file).extract(osz_file) as beatmap:
                Logger.mappa_pakka.info(f"File {beatmap} marked as temporary")
                return cls(map_id, beatmap, temporary=True)

        return cls(map_id, osz_file, temporary=False)


class Maps:
    def __init__(self, maps: List[Map]):
        self.maps = maps

    @classmethod
    async def from_map_ids(cls, map_ids: Iterable) -> "Maps":
        valid_map_ids = list(filter(lambda map_id: map_id is not None, map_ids))
        Logger.mappa_pakka.info(f"Downloading maps {map_ids}")
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
        Logger.mappa_pakka.info(files)
        FileTools.zip_files(files, to_file=map_pack_file)

        return map_pack_file

    def cleanup(self):
        Logger.mappa_pakka.info("Cleaning up files")
        for item in self.maps:
            if item.temporary and item.osz_file.exists():
                item.osz_file.unlink()
