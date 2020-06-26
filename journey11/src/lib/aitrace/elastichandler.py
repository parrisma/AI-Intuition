from logging import Handler
from elasticsearch import Elasticsearch


class ElasticHandler(Handler):
    def __init__(self,
                 elastic_server_utl: str,
                 log_index_name: str):
        """
        Connect to given Elastic instance.
        :param elastic_server_utl: The URL of the Elastic server e.g. http://localhost:9200
        :param log_index_name: The name of the elastic index to write logs to
        """
        Handler.__init__(self)
        self._es = Elasticsearch([elastic_server_utl])
        self._es_index = log_index_name
        return

    def emit(self, record):
        msg = self.formatter.format(record=record)
        self._es.create(index=self._es_index,
                        body=msg,
                        id=1)
        return
