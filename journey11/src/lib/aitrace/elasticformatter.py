from abc import ABC, abstractmethod
from datetime import datetime
from logging import Formatter
from typing import Dict, List
import pytz
import json


class ElasticFormatter(Formatter):
    class ElasticDateFormatter(ABC):

        @abstractmethod
        def format(self, dtm) -> str:
            pass

    class DefaultElasticDateFormatter(ElasticDateFormatter):

        def format(self, dtm) -> str:
            if isinstance(dtm, float):
                dtm = datetime.fromtimestamp(dtm)
            elif not isinstance(dtm, datetime):
                raise ValueError(
                    "Log created date must be supplied as float (timestamp) or datetime not {}".format(str(type(dtm))))
            return self._elastic_time_format(pytz.utc.localize(dtm))

        @staticmethod
        def _elastic_time_format(dt: datetime) -> str:
            return dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    _jflds = ["session_uuid", "level", "timestamp", "message"]
    # Allow cross platform consistency of logging levels
    _level_map = {50: "CRITICAL",
                  40: "ERROR",
                  30: "WARNING",
                  20: "INFO",
                  10: "DEBUG",
                  0: "NOTSET"
                  }

    def __init__(self,
                 level_map: Dict = None,
                 json_field_names: List = None,
                 date_formatter: ElasticDateFormatter = None):
        """
        Boostrap Elastic Log Formatter
        :param level_map: Dictionary of log level numbers to string equivalent : None => use str(level_no)
        :param json_field_names: Names of 4 json fields in order [session_uuid, type_uuid, timestamp, message].
                                 None implies use the field names as show in this description
        :param date_formatter: Takes a datetime and return as string - if None fmt = %Y-%m-%dT%H:%M:%S.%f%z
        """
        super(ElasticFormatter, self).__init__()

        if json_field_names is None or len(json_field_names) == 0:
            self.json_fields = self._jflds
        else:
            self.json_fields = json_field_names

        self._fmt = '{{{{"{}":"{{}}","{}":"{{}}","{}":"{{}}","{}":"{{}}"}}}}'.format(self._jflds[0], self._jflds[1],
                                                                                     self._jflds[2], self._jflds[3])

        if date_formatter is None:
            self._date_formatter = ElasticFormatter.DefaultElasticDateFormatter()
        else:
            self._date_formatter = date_formatter

        if level_map is None or len(level_map) == 0:
            self._level_map = self.default_level_map()
        else:
            self._level_map = level_map
        return

    @staticmethod
    def default_level_map() -> Dict:
        return ElasticFormatter._level_map

    def _translate_level_no(self,
                            level_no: int) -> str:
        """
        Translate a logging level number into a uuid event type
        :param level_no: The level no to translate
        :return: UUID equivalent of the level no.
        """
        if self._level_map is not None:
            res = self._level_map.get(level_no, str(level_no))
        else:
            res = str(level_no)
        return res

    def format(self, record):
        """
        Extract Record (name, level, timestamp and message) and format as json ready to be written to elastic DB
        :param record: The logging record to parse
        :return: The log entry as JSON
        """
        sess_n = record.name
        type_n = self._translate_level_no(record.levelno)
        trace_date = self._date_formatter.format(record.created)
        message = json.dumps(record.msg)[1:-1]  # ensure special characters are escaped eg ' & "
        json_msg = self._fmt.format(sess_n, type_n, trace_date, message)
        return json_msg
