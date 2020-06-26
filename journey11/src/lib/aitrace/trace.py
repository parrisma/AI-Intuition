import logging
import sys
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.aitrace.elasticformatter import ElasticFormatter
from journey11.src.lib.aitrace.elastichandler import ElasticHandler


class Trace:
    # Annotation
    _CONSOLE_FORMATTER: logging.Formatter
    _logger: logging.Logger

    _CONSOLE_FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s", datefmt='%Y-%m-%dT%H:%M:%S%z')
    _ELASTIC_FORMATTER = ElasticFormatter()
    _logger = None
    _with_elastic = None

    @classmethod
    def __init__(cls,
                 with_elastic: bool = True):
        cls._with_elastic = with_elastic
        cls._bootstrap()
        return

    @classmethod
    def _bootstrap(cls):
        if Trace._logger is None:
            Trace._logger = logging.getLogger(UniqueRef().ref)
            Trace._logger.setLevel(logging.DEBUG)
            Trace._logger.addHandler(cls.get_console_handler())
            if cls._with_elastic:
                Trace._logger.addHandler(cls.get_elastic_handler())
            Trace._logger.propagate = False
        return

    @classmethod
    def get_console_handler(cls):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(Trace._CONSOLE_FORMATTER)
        return console_handler

    @classmethod
    def get_elastic_handler(cls):
        elastic_handler = ElasticHandler('http://localhost:9200', 'trace_log')
        elastic_handler.setFormatter(Trace._ELASTIC_FORMATTER)
        return elastic_handler

    @classmethod
    def log(cls) -> logging.Logger:
        if Trace._logger is None:
            cls._bootstrap()
        return Trace._logger
