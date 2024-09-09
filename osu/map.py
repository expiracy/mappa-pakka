import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, List

from config_example import MAP_PACKS_FOLDER
from helper.tools import FileTools
from osu.beatmap_extractor import BeatmapExtractor
from osu.client import OsuClient
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
            print(f"Extracting beatmap from osz: {map_id}")
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
        FileTools.delete_files(files)

        return map_pack_file
