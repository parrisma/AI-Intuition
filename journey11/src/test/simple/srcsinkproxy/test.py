import unittest
import logging
from src.lib.aitrace.trace import Trace
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy
from journey11.src.test.kpubsub.test import KPuBsubUtil
from journey11.src.test.srcsink.testsrcsink import TestSrcSink


class TestSimpleSrcSinkProxy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Trace()

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
                                                    num_msg=50)
        self.assertTrue(len(expected) == len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
        return


if __name__ == "__main__":
    unittest.main()
