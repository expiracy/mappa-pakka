import io
import re
import zipfile
from pathlib import Path
from typing import List, Iterable


class FileTools:
    @staticmethod
    def zip_files(files: Iterable[Path], to_file: Path):
        with zipfile.ZipFile(to_file, 'w') as zf:
            for file in files:
                zf.write(file, arcname=file.name)

    @staticmethod
    def delete_files(files: Iterable[Path]):
        for file in files:
            file.unlink()

    @staticmethod
    def clean_path_string(path: str):
        return re.sub(r"[/\\<>:]", "_", path)

