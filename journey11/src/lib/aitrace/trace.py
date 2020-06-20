import logging
import sys
from journey11.src.lib.namegen.namegen import NameGen


class Trace:
    # Annotation
    _FORMATTER: logging.Formatter
    _logger: logging.Logger

    _FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
    _logger = None

    @classmethod
    def __init__(cls):
        cls._bootstrap()
        return

    @classmethod
    def _bootstrap(cls):
        if Trace._logger is None:
            Trace._logger = logging.getLogger(NameGen.generate_random_name())
            Trace._logger.setLevel(logging.DEBUG)
            Trace._logger.addHandler(cls.get_console_handler())
            Trace._logger.propagate = False
        return

    @classmethod
    def get_console_handler(cls):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(Trace._FORMATTER)
        return console_handler

    @classmethod
    def log(cls) -> logging.Logger:
        if Trace._logger is None:
            cls._bootstrap()
        return Trace._logger
