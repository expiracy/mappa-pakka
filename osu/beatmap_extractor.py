import re
import zipfile
from pathlib import Path

from osu.map_id import BeatmapId


class BeatmapExtractor:
    def __init__(self, beatmap_id: BeatmapId, osz_file: Path):
        self.beatmap_id = beatmap_id
        self.osz_file = self.extract(osz_file)

    def extract(self, beatmapset_osz_file: Path) -> Path:
        beatmap_osz_file = beatmapset_osz_file.with_stem(f"[{self.beatmap_id.beatmap_id}] {beatmapset_osz_file.stem}")
        osu_file_found = False

        beatmap_id_pattern = re.compile(r"BeatmapID:\s*([0-9]+)")

        with zipfile.ZipFile(beatmapset_osz_file, 'r') as zf:
            with zipfile.ZipFile(beatmap_osz_file, 'w') as zf_out:
                for file in zf.infolist():
                    filename = file.filename

                    if filename.endswith(".osu"):
                        osu_file_found = True
                        file_content = zf.read(filename).decode('utf-8', errors='ignore')

                        found_beatmap_id = int(beatmap_id_pattern.search(file_content).group(1))
                        if self.beatmap_id.beatmap_id == found_beatmap_id:
                            zf_out.writestr(filename, file_content.encode('utf-8'))
                    else:
                        zf_out.writestr(filename, zf.read(filename))

        file_to_return = beatmap_osz_file if osu_file_found else self.osz_file
        return file_to_return
