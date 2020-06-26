from typing import Dict, Callable, IO
from datetime import datetime
import pytz
from elasticsearch import Elasticsearch


class ESUtil:
    # Annotations
    _es: Dict[str, Elasticsearch]

    _es = dict()

    @classmethod
    def get_connection(cls,
                       hostname: str,
                       port_id: str) -> Elasticsearch:
        """
        Get the default Elastic host and port from the environment elastic settings Yaml and make an
        Elasticsearch connection to that return host and port
        :return: The Elasticsearch connection object for default host and port
        """
        connection_str = "{}:{}".format(hostname, port_id)
        if cls._es.get(connection_str, None) is None:
            try:
                cls._es[connection_str] = Elasticsearch([connection_str])
            except Exception as e:
                raise RuntimeError("Failed to open Elastic search connection {}:{}".format(hostname, port_id))
        return cls._es[connection_str]

    @staticmethod
    def load_json(json_stream: Callable[[], IO[str]]) -> str:
        """
        Read the given JSON stream and return contents as string
        :param json_stream: A callable that returns an open stream to the YAML source
        :return: The contents of the Json file as string.
        """
        res = str()
        try:
            _stream = json_stream()
            for _line in _stream:
                res += _line.decode("utf-8")
        except Exception as e:
            raise RuntimeError("Unable to read json from given stream")
        return res

    @staticmethod
    def datetime_in_elastic_time_format(dt: datetime) -> str:
        """
        Return a datetime in format to be written to elastic as timezone aware
        :param dt:
        :return:
        """
        return pytz.utc.localize(dt).strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    @staticmethod
    def create_index_from_json(es: Elasticsearch,
                               idx_name: str,
                               json_stream: Callable[[], IO[str]]) -> bool:
        """

        :param es: An valid elastic search connection
        :param idx_name: The name of the index to create
        :param json_stream: A callable that returns an open stream to the YAML source
        :return: True if created or if index already exists
        """
        try:
            body = ESUtil.load_json(json_stream)

            # Exception will indicate index create error.
            _ = es.indices.create(index=idx_name,
                                  body=body,
                                  wait_for_active_shards=1,
                                  ignore=[400, 404])
        except Exception as e:
            raise RuntimeError(
                "Failed to create elastic index [{}] from Json stream".format(idx_name))
        return True
