import unittest
import logging
import kpubsubai
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy
from journey11.src.test.kpubsub.test import KPuBsubUtil
from journey11.src.test.srcsink.testsrcsink import TestSrcSink


class TestSimpleSrcSinkProxy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    @staticmethod
    def _factory() -> SimpleSrcSinkProxy:
        """
        Generate a random instance of a SimpleSrcSinkProxy
        :return: A new SimpleSrcSinkProxy
        """
        return SimpleSrcSinkProxy(srcsink=TestSrcSink())

    def test_pubsub_transport(self):
        """
        Generate random SimpleSrcSinkProxies and ensure that all serialize/deserialize correctly.
        The requires the containerized test Kafka Service to be running locally.
        """
        logging.info("SimpleSrcSinkProxy Test: Case 1")
        expected = list()
        actual = list()
        expected, actual = KPuBsubUtil.kpubsub_test(msg_factory=self._factory,
                                                    num_msg=50,
                                                    msg_map_url=kpubsubai.MSG_MAP_URL)
        self.assertTrue(len(expected) == len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
        return


if __name__ == "__main__":
    unittest.main()
