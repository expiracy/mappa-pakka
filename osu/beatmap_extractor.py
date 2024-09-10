"""
Hey James xoxo
I will code the extractor in the following way
You pass in a zip file to all the .osz archives
and it will spit out a zip file of directories of osu maps!!
Love
Tingyi xxxxxx

Important documentation:
Due to how things are passed in with the unzip function, we need to ensure
that the archive being passed in MUST correspond with the list of beatmap
IDs that is also passed in

i.e
we need to pull beatmapID 69 out of mapset1, and beatmapID 420 out of mapset2.
our archive would look like this:

mapset1
mapset2

and our array of IDs must look like this:
[69, 420]
for it to pull beatmapID 69 out of mapset1, and beatmapID 420 out of mapset2.
"""
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

        # Delete the unused osz file and return the correct one

        if not osu_file_found:
            beatmap_osz_file.unlink()
            return self.osz_file
        else:
            beatmapset_osz_file.unlink()
            return beatmap_osz_file
