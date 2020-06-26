import numpy as np
import pytz
from datetime import datetime, timedelta, timezone
from elasticsearch import Elasticsearch
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.namegen.namegen import NameGen
from journey11.src.test.gibberish.gibberish import Gibberish


class Json2Elastic:
    _headers = {'Content-Type': 'application/json'}
    operation_timeout = 60

    def __init__(self,
                 num_session: int = 100,
                 num_type: int = 10):
        self._es = Elasticsearch(['http://localhost:9200'])
        self._sessions = list()
        self._num_session = num_session
        self._num_type = num_type
        for _ in range(self._num_session):
            self._sessions.append(UniqueRef().ref)
        self._types = list()
        for _ in range(self._num_type):
            self._types.append(UniqueRef().ref)
        self._start_date = pytz.utc.localize(datetime(2020, 1, 1))
        self._end_date = pytz.utc.localize(datetime(2020, 7, 1))
        self._days = (self._end_date - self._start_date).days
        return

    @staticmethod
    def load_json(filename: str) -> str:
        res = str()
        for l in open(filename, "r"):
            res += l
        return res

    def rnd_time(self) -> datetime:
        return self._start_date + timedelta(days=np.floor(self._days * np.random.random()),
                                            hours=np.floor(60 * np.random.random()),
                                            minutes=np.floor(60 * np.random.random()),
                                            seconds=np.floor(60 * np.random.random()),
                                            milliseconds=np.floor(1000 * np.random.random()))

    @staticmethod
    def elastic_time_format(dt: datetime) -> str:
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

    def get_idx(self,
                idx_name: str) -> str:
        res = None
        try:
            res = self._es.search(index=idx_name, body={"query": {"match_all": {}}})
        except Exception as e:
            print(str(e))
        return res

    def create_idx(self,
                   idx_name: str = None) -> str:
        if idx_name is None:
            idx_name = NameGen.generate_random_name().lower()

        body = Json2Elastic.load_json("tracelog_mapping.json")
        try:
            res = self._es.indices.create(index=idx_name,
                                          body=body,
                                          wait_for_active_shards=1,
                                          ignore=[400])
        except Exception as e:
            print(str(e))
        return idx_name

    def random_trace_message(self) -> str:
        sess_n = self._sessions[np.random.randint(low=1, high=self._num_session, size=1)[0]]
        type_n = self._types[np.random.randint(low=1, high=self._num_type, size=1)[0]]
        trace_date = Json2Elastic.elastic_time_format(self.rnd_time())
        message = Gibberish.more_gibber()
        json_trace_doc = '{{"session_uuid":"{}","type_uuid":"{}","timestamp":"{}","message":"{}"}}'.format(sess_n,
                                                                                                           type_n,
                                                                                                           trace_date,
                                                                                                           message)
        return json_trace_doc

    def insert_trace_records(self,
                             idx_name: str) -> None:
        for n in range(1000):
            if n % 100 == 0:
                print("Added {}".format(n))
            doc = self.random_trace_message()
            res = self._es.create(index=idx_name,
                                  body=doc,
                                  id=UniqueRef().ref)
        return


if __name__ == "__main__":
    j2e = Json2Elastic()
    idx_name = j2e.create_idx("trace_log")
    print(j2e.get_idx(idx_name=idx_name))
    j2e.insert_trace_records(idx_name=idx_name)
