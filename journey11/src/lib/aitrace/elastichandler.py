from logging import Handler
from elasticsearch import Elasticsearch


class ElasticHandler(Handler):
    def __init__(self,
                 elastic_connection: Elasticsearch,
                 log_index_name: str):
        """
        Connect to given Elastic instance.
        :param elastic_connection: An elastic search connection object
        :param log_index_name: The name of the elastic index to write logs to
        """
        Handler.__init__(self)
        self._es = elastic_connection
        self._es_index = log_index_name
        return

    def emit(self, record):
        msg = self.formatter.format(record=record)
        try:
            res = self._es.index(index=self._es_index,
                                 body=msg)
        except Exception as e:
            raise RuntimeError("Failed to write log to Elastic")
        return
