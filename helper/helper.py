import io
import zipfile
from pathlib import Path
from typing import List

from config_example import MAP_PACKS_FOLDER


class Tools:
    @staticmethod
    def zip_files(files: List[Path], to_file: Path):
        with zipfile.ZipFile(to_file, 'w') as zf:
            for file in files:
                zf.write(file, arcname=file.name)
