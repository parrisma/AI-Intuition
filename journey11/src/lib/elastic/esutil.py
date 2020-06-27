from typing import Dict, Callable, IO, List
from datetime import datetime
import pytz
import re
from elasticsearch import Elasticsearch


class ESUtil:
    # Annotations
    _es: Dict[str, Elasticsearch]

    _es = dict()
    _ALL = 10000
    _COUNT = 0

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
    def json_insert_args(json_source: str,
                         **kwargs) -> str:
        """
        Replace all parameters in kwargs with name that matches arg<999> with the value of the parameter
        where the marker in the source json is of the form <0> = arg0, <1> = arg1 etc
        :param json_source: The Json source to do parameter insertion on
        :param kwargs: arbitrary arguments to insert that match pattern arg0, arg1, arg2, ...
        :return: Source json with the arguments substituted
        """
        arg_pattern = re.compile("^arg[0-9]+$")
        for k, v in kwargs.items():
            if arg_pattern.search(k):
                repl_re = "(<{}>)".format(k)
                json_source = re.sub(repl_re, v, json_source)
        return json_source

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

        :param es: An open elastic search connection
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

    @staticmethod
    def run_search(es: Elasticsearch,
                   idx_name: str,
                   json_query: str,
                   **kwargs) -> List[Dict]:
        """

        :param es: An open elastic search connection
        :param idx_name: The name of the index to execute search on
        :param json_query: The Json query to run
        :param kwargs: arguments to the json_query of the form arg0='value 0', arg1='value 1' .. argn='value n'
                       where the argument values will be substituted into the json query before it is executed.
                       The raw query { x: { y: <arg0> } } will have <arg0> fully replaced with the corresponding
                       kwargs value supplied for all arg0..argn. Where there are multiple occurrences of any <argn>
                       all occurrences will be replaced.
        :return: Raise an exception on error
        """
        try:
            json_query_to_execute = ESUtil.json_insert_args(json_source=json_query, **kwargs)
            # Exception will indicate search error.
            res = es.search(index=idx_name,
                            body=json_query_to_execute,
                            size=ESUtil._ALL)
        except Exception as e:
            raise RuntimeError(
                "Failed to execute query [{}] on Index [{}]".format(json_query, idx_name))
        return list(res['hits']['hits'])
