import logging
import sys
from datetime import datetime

import config
from config import ROOT
from helper.tools import FileTools


class Logger:
    mappa_pakka = logging.getLogger('mappa-pakka')

    @classmethod
    def setup(cls, to_file=False):
        fmt = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
        formatter = logging.Formatter(
            fmt=fmt,
            datefmt='%Y-%m-%d %H:%M:%S'  # Custom date format
        )

        logging.basicConfig(level=logging.WARNING, format=fmt)
        cls.mappa_pakka.setLevel(logging.DEBUG)

        if to_file:
            clean_date = FileTools.clean_path_string(str(datetime.now()))
            log_file = config.LOG_FOLDER.joinpath(f"mappa-pakka [{clean_date}].log")
            cls.mappa_pakka.info(f"Logging to file: {log_file}")
            handler = logging.FileHandler(
                filename=log_file,
                encoding='utf-8',
                mode='w'
            )
            handler.setFormatter(formatter)
            cls.mappa_pakka.addHandler(handler)


Logger.setup(to_file=True)
