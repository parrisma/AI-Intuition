from typing import Dict
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
    def load_json(filename: str) -> str:
        """
        Read the given JSON file and return contents as string
        :param filename: The Json file to load.
        :return: The contents of the Json file as string.
        """
        res = str()
        try:
            for l in open(filename, "r"):
                res += l
        except Exception as e:
            raise RuntimeError("Unable to open json file : {}".format(filename))
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
                               json_filename: str) -> bool:
        """

        :param es: An valid elastic search connection
        :param idx_name: The name of the index to create
        :param json_filename: The json file that contains the index definition
        :return: True if created or if index already exists
        """
        try:
            body = ESUtil.load_json(json_filename)

            # Exception will indicate index create error.
            _ = es.indices.create(index=idx_name,
                                  body=body,
                                  wait_for_active_shards=1,
                                  ignore=[400, 404])
        except Exception as e:
            raise RuntimeError(
                "Failed to create elastic index [{}] from Json file [{}}".format(idx_name, json_filename))
        return True
