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
import zipfile
from pathlib import Path

from osu.map_id import BeatmapId


class BeatmapExtractor:
    def __init__(self, beatmap_id: BeatmapId, osz_file: Path):
        self.beatmap_id = beatmap_id
        self.osz_file: Path = osz_file

    def get_beatmap_file(self) -> Path:
        new_osz_file = self.osz_file.with_stem(f"[{self.beatmap_id.beatmap_id}] {self.osz_file.stem}")
        osu_file_found = False

        with zipfile.ZipFile(self.osz_file, 'r') as zf:
            with zipfile.ZipFile(new_osz_file, 'w') as zf_out:
                for file in zf.infolist():
                    filename = file.filename

                    if filename.endswith(".osu"):
                        osu_file_found = True
                        file_content = zf.read(filename).decode('utf-8', errors='ignore')

                        if str(self.beatmap_id.beatmap_id) in file_content:
                            zf_out.writestr(filename, file_content.encode('utf-8'))
                    else:
                        zf_out.writestr(filename, zf.read(filename))

        if not osu_file_found:
            new_osz_file.unlink()
            return self.osz_file

        return new_osz_file
