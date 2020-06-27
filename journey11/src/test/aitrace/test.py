import unittest
import json
import time
from typing import List, Dict
from datetime import datetime
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.envboot.envbootstrap import EnvBootstrap
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.elastic.esutil import ESUtil
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from journey11.src.lib.aitrace.elasticformatter import ElasticFormatter
from journey11.src.test.run_spec.runspec import RunSpec


class TestAITrace(unittest.TestCase):
    class DummyLoggingRecord:
        # Proxy/model for the Python logging Record (only relevant fields set here)
        def __init__(self,
                     name: str,
                     level_no: int,
                     message: str,
                     created: datetime):
            self.name = name
            self.levelno = level_no
            self.msg = message
            self.created = created
            return

    @classmethod
    def setUpClass(cls):
        EnvBootstrap()
        return

    def test_elastic_formatter(self):
        ef = ElasticFormatter()
        record = TestAITrace.DummyLoggingRecord(name="de741e6c74164189827100ba65eda743",
                                                level_no=10,
                                                message="c5ee7458-1c4a-453a-8582-ebe7744e3623",
                                                created=datetime(year=2000, month=6, day=20,
                                                                 hour=18, minute=37, second=51, microsecond=67)
                                                )
        res = ef.format(record=record)
        self.assertEqual(
            '{"session_uuid":"de741e6c74164189827100ba65eda743","level":"DEBUG","timestamp":"2000-06-20T18:37:51.000067+0000","message":"c5ee7458-1c4a-453a-8582-ebe7744e3623"}',
            res)
        js = json.loads(res)
        self.assertEqual(js['session_uuid'], "de741e6c74164189827100ba65eda743")
        self.assertEqual(js['level'], "DEBUG")
        self.assertEqual(js['timestamp'], "2000-06-20T18:37:51.000067+0000")
        self.assertEqual(js['message'], "c5ee7458-1c4a-453a-8582-ebe7744e3623")
        return

    def test_elastic_formatter_special_character(self):
        """
        Need to ensure JSON special characters are encoded correctly
        """
        ef = ElasticFormatter()
        record = TestAITrace.DummyLoggingRecord(name="de741e6c74164189827100ba65eda743",
                                                level_no=10,
                                                message=chr(34) + chr(32) + chr(39) + chr(32) + chr(92),
                                                created=datetime(year=2000, month=6, day=20,
                                                                 hour=18, minute=37, second=51, microsecond=67)
                                                )
        res = ef.format(record=record)
        self.assertEqual(
            '{"session_uuid":"de741e6c74164189827100ba65eda743","level":"DEBUG","timestamp":"2000-06-20T18:37:51.000067+0000","message":"\\" \' \\\\"}',
            res)
        js = json.loads(res)
        self.assertEqual(js['session_uuid'], "de741e6c74164189827100ba65eda743")
        self.assertEqual(js['level'], "DEBUG")
        self.assertEqual(js['timestamp'], "2000-06-20T18:37:51.000067+0000")
        self.assertEqual(js['message'],
                         chr(34) + chr(32) + chr(39) + chr(32) + chr(92))  # should be un encoded as parsed
        return

    def test_json_insert_args(self):
        str_to_insert_into = "0=<arg0> 2=<arg2> 1=<arg1> 10=<arg10> 2=<arg2><arg2> 20=<arg20>"
        actual = ESUtil.json_insert_args(str_to_insert_into,
                                         arg10="10",
                                         argument0="ShouldIgnoreMe",
                                         arg2="2",
                                         arg0="0",
                                         arg1="1",
                                         ar0="ShouldIgnoreMe")
        self.assertEqual("0=0 2=2 1=1 10=10 2=22 20=<arg20>", actual)
        return

    def test_elastic(self):
        """
        Write 100 records to Trace, which is elastic enabled and check that 100 matching records appear in
        the appropriate index.
        """
        _num_to_create = 100
        try:
            correlation_ref = UniqueRef().ref
            for i in range(_num_to_create):
                Trace.log().debug("{}-{}".format(correlation_ref, i))
            time.sleep(1)
            res = self._test_search(correlation_ref=correlation_ref)
            self.assertEqual(_num_to_create, len(res))
        except Exception as e:
            self.assertFalse("Unexpected Exception while testing Trace logging")
        return

    def _test_search(self,
                     correlation_ref: str) -> List[Dict]:
        """
        Look for the records inserted with message containing the given correlation ref.
        :param correlation_ref: The correlation refernce to search for
        """
        json_query = """{
            "query": {
                "wildcard": {
                    "message": "*<arg0>*"
                }
            }
        }"""

        settings = Settings(settings_yaml_stream=WebStream(RunSpec.trace_settings_yaml()),
                            bespoke_transforms=RunSpec.setting_transformers())
        elastic_index_name, _ = settings.default()

        es = EnvBootstrap.get_context()[EnvBuilder.ElasticDbConnectionContext]
        res = ESUtil.run_search(es=es,
                                idx_name=elastic_index_name,
                                json_query=json_query,
                                arg0=correlation_ref)
        return res


if __name__ == "__main__":
    unittest.main()
