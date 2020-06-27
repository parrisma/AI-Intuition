import logging
import sys
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.aitrace.elasticformatter import ElasticFormatter
from journey11.src.lib.aitrace.elastichandler import ElasticHandler


class Trace:
    # Annotation
    _CONSOLE_FORMATTER: logging.Formatter
    _logger: logging.Logger
    _console_handler: logging.Handler
    _elastic_handler: logging.Handler

    _CONSOLE_FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s",
                                           datefmt='%Y-%m-%dT%H:%M:%S%z')
    _ELASTIC_FORMATTER = ElasticFormatter()
    _logger = None
    _console_handler = None
    _elastic_handler = None

    @classmethod
    def __init__(cls,
                 with_elastic: bool = True):
        cls._bootstrap()
        return

    @classmethod
    def _bootstrap(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger(UniqueRef().ref)
            cls._logger.setLevel(logging.DEBUG)
            cls.enable_console_handler()
        return

    @classmethod
    def enable_console_handler(cls) -> None:
        if cls._console_handler is None:
            cls._console_handler = logging.StreamHandler(sys.stdout)
            cls._console_handler.setFormatter(Trace._CONSOLE_FORMATTER)
            Trace._logger.addHandler(cls._console_handler)
        return

    @classmethod
    def enable_elastic_handler(cls,
                               elastic_handler: ElasticHandler) -> None:
        if cls._elastic_handler is None:
            cls._elastic_handler = elastic_handler
            cls._elastic_handler.setFormatter(Trace._ELASTIC_FORMATTER)
            Trace._logger.addHandler(cls._elastic_handler)
        return

    @classmethod
    def log(cls) -> logging.Logger:
        if Trace._logger is None:
            cls._bootstrap()
        return Trace._logger
