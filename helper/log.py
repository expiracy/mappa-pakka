import logging
import sys

from config import ROOT


class Logger:
    format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
    logger = logging.getLogger('mappa-pakka')

    @classmethod
    def setup(cls, to_file = False):
        logging.basicConfig(level=logging.WARNING, format=cls.format)
        cls.logger.setLevel(logging.DEBUG)

        if to_file:
            logs_path = ROOT.joinpath("logs")
            logs_path.mkdir(exist_ok=True, parents=True)

            handler = logging.FileHandler(filename=logs_path.joinpath("mappa-pakka.log"), encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter(cls.format))
            cls.logger.addHandler(handler)


Logger.setup()
