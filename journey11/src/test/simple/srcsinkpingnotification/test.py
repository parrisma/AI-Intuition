import unittest
import logging
import numpy as np
import kpubsubai
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy
from journey11.src.main.simple.simplesrcsinkpingnotification import SimpleSrcSinkPingNotification
from journey11.src.test.kpubsub.test import KPuBsubUtil
from journey11.src.test.srcsink.testsrcsink import TestSrcSink
from journey11.src.test.gibberish.gibberish import Gibberish


class TestSimpleSrcSinkPingNotification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    @staticmethod
    def _address_book() -> [SimpleSrcSinkProxy]:
        """
        Generate a random list of SimpleSrcSinkProxies as an address book
        :return: A new UniqueWorkRef
        """
        addresses = list()
        for i in range(np.random.randint(10)):
            addresses.append(SimpleSrcSinkProxy(srcsink=TestSrcSink()))
        return addresses

    @staticmethod
    def _factory() -> SimpleSrcSinkPingNotification:
        """
        Generate a random instance of a SimpleSrcSinkPingNotification
        :return: A new SimpleSrcSinkProxy
        """
        return SimpleSrcSinkPingNotification(work_ref=UniqueWorkRef(prefix=Gibberish.word_gibber()),
                                             responder_srcsink=TestSrcSink(),
                                             address_book=TestSimpleSrcSinkPingNotification._address_book())

    def test_pubsub_transport(self):
        """
        Generate random SrcSinkPingNotifications and ensure that all serialize/deserialize correctly.
        The requires the containerized test Kafka Service to be running locally.
        """
        logging.info("SrcSinkPingNotification Test: Case 1")
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
