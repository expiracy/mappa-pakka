import re
import zipfile
from pathlib import Path

from helper.log import Logger
from osu.map_id import BeatmapId
from osu.osu_client import OsuClient


class BeatmapNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BeatmapExtractor:
    def __init__(self, beatmap_id: BeatmapId, osz_file: Path):
        self.beatmap_id = beatmap_id
        self.osz_file = self.extract(osz_file)

    def extract(self, beatmapset_osz_file: Path) -> Path:
        try:
            return self.try_extract(beatmapset_osz_file)
        except BeatmapNotFoundException as e:
            Logger.mappa_pakka.warning(e)

        try:
            return self.extract_legacy(beatmapset_osz_file)
        except BeatmapNotFoundException as e:
            Logger.mappa_pakka.error(e)

        return beatmapset_osz_file

    def try_extract(self, in_osz_file: Path) -> Path:
        out_osz_file = in_osz_file.with_stem(f"[{self.beatmap_id.beatmap_id}] {in_osz_file.stem}")
        found = False
        beatmap_id_pattern = re.compile(r"BeatmapID:\s*([0-9]+)")

        with zipfile.ZipFile(in_osz_file, 'r') as zf_in:
            with zipfile.ZipFile(out_osz_file, 'w') as zf_out:

                for file in zf_in.infolist():
                    filename = file.filename

                    if filename.endswith(".osu"):
                        file_content = zf_in.read(filename).decode('utf-8', errors='ignore')

                        maybe_beatmap_id = beatmap_id_pattern.search(file_content)

                        if maybe_beatmap_id is None:
                            raise BeatmapNotFoundException(f"Beatmap [{filename}] does not contain a beatmap ID")

                        found = True
                        found_beatmap_id = int(maybe_beatmap_id.group(1))

                        if self.beatmap_id.beatmap_id == found_beatmap_id:
                            zf_out.writestr(filename, file_content.encode('utf-8'))

                    else:
                        zf_out.writestr(filename, zf_in.read(filename))

        if not found:
            raise BeatmapNotFoundException(f"Beatmap [{filename}] was not found in beatmapset [{str(in_osz_file)}]")

        return out_osz_file

    def extract_legacy(self, in_osz_file: Path) -> Path:
        out_osz_file = in_osz_file.with_stem(f"[{self.beatmap_id.beatmap_id}] {in_osz_file.stem}")
        beatmap = OsuClient.get_beatmap_sync(self.beatmap_id.beatmap_id)
        beatmapset = beatmap.beatmapset()
        expected_file_name = f"{beatmapset.artist} - {beatmapset.title} ({beatmapset.creator.title()}) [{beatmap.version}].osu"
        found = False

        Logger.mappa_pakka.info(f"Extracting legacy beatmap [{expected_file_name}] from beatmapset [{in_osz_file}]")

        with zipfile.ZipFile(in_osz_file, 'r') as zf_in:
            with zipfile.ZipFile(out_osz_file, 'w') as zf_out:

                for file in zf_in.infolist():
                    filename = file.filename

                    if not filename.endswith(".osu"):
                        zf_out.writestr(filename, zf_in.read(filename))
                    else:
                        if found:
                            continue

                        file_content = zf_in.read(filename).decode('utf-8', errors='ignore')

                        if filename == expected_file_name:
                            found = True
                            zf_out.writestr(filename, file_content.encode('utf-8'))

        if not found:
            raise BeatmapNotFoundException(f"Beatmap [{filename}] was not found in beatmapset [{str(in_osz_file)}] using legacy extraction method")

        return out_osz_file
