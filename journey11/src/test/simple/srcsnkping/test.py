import unittest
import logging
import numpy as np
import kpubsubai
from journey11.src.interface.capability import Capability
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.main.simple.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.test.kpubsub.test import KPuBsubUtil
from journey11.src.test.srcsink.testsrcsink import TestSrcSink
from journey11.src.test.gibberish.gibberish import Gibberish


class TestSimpleSrcSinkPing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    @staticmethod
    def _capabilities() -> [Capability]:
        """
        Generate a random list of Capabilities
        :return: A new UniqueWorkRef
        """
        caps = list()
        for i in range(np.random.randint(10)):
            caps.append(SimpleCapability(uuid=UniqueRef().ref, capability_name=Gibberish.word_gibber()))
        return caps

    @staticmethod
    def _factory() -> SimpleSrcSinkPing:
        """
        Generate a random instance of a SimpleSrcSinkPing
        :return: A new SimpleSrcSinkProxy
        """
        return SimpleSrcSinkPing(sender_srcsink=TestSrcSink(),
                                 required_capabilities=TestSimpleSrcSinkPing._capabilities())

    def test_pubsub_transport(self):
        """
        Generate 1000 random SrcSinkPings and ensure that all serialize/deserialize correctly.
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