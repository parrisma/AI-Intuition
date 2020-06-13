import unittest
import numpy as np
import logging
import kpubsubai
from journey11.src.interface.capability import Capability
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.test.kpubsub.test import TestKPubSub
from journey11.src.test.gibberish.gibberish import Gibberish


class TestCapability(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_simple(self):
        capability_name = "DummyCapability1"
        test_capability = SimpleCapability(uuid=UniqueRef().ref, capability_name=capability_name)
        self.assertEqual(capability_name, test_capability.value())
        return

    def test_equality_same_type(self):
        capability_name_one = "DummyCapability1"
        capability_name_two = "DummyCapability2"
        test_capability_1 = SimpleCapability(uuid=UniqueRef().ref, capability_name=capability_name_one)
        test_capability_2 = SimpleCapability(uuid=UniqueRef().ref, capability_name=capability_name_one)
        test_capability_3 = SimpleCapability(uuid=UniqueRef().ref, capability_name=capability_name_two)
        self.assertEqual(True, test_capability_1 == test_capability_2)
        self.assertEqual(True, test_capability_1 != test_capability_3)
        return

    def test_equality_diff_type(self):
        capability_name_one = "DummyCapability1"
        test_capability_1 = SimpleCapability(uuid=UniqueRef().ref, capability_name=capability_name_one)
        self.assertEqual(True, test_capability_1 != capability_name_one)
        self.assertEqual(True, test_capability_1 != int(1))
        return

    def test_equiv_degree_no_given(self):
        """
        Test the equivalency factor calc.
        """
        cap1 = SimpleCapability(uuid=UniqueRef().ref, capability_name="Cap_one")
        cap2 = SimpleCapability(uuid=UniqueRef().ref, capability_name="Cap_two")
        cap3 = SimpleCapability(uuid=UniqueRef().ref, capability_name="Cap_three")
        cap4 = SimpleCapability(uuid=UniqueRef().ref, capability_name="Cap_four")
        cap5 = SimpleCapability(uuid=UniqueRef().ref, capability_name="Cap_five")

        scenarios = [[None, None, float(1)],
                     [None, [], float(1)],
                     [None, [cap1], float(1)],
                     [None, [cap1, cap2, cap3, cap4, cap5], float(1)],
                     [[], [cap1], float(1)],
                     [[], [cap1, cap2, cap3, cap4, cap5], float(1)],
                     [[cap1], None, float(0)],
                     [[cap1, cap2, cap3, cap4, cap5], None, float(0)],
                     [[cap1], [], float(0)],
                     [[cap1, cap2, cap3, cap4, cap5], [], float(0)],
                     [[cap1], [cap1], float(1 / 1)],
                     [[cap1, cap2], [cap1], float(1 / 2)],
                     [[cap1, cap2, cap3], [cap1], float(1 / 3)],
                     [[cap1, cap2, cap3, cap4], [cap1], float(1 / 4)],
                     [[cap1, cap2, cap3, cap4, cap5], [cap1], float(1 / 5)],
                     [[cap1], [cap1, cap2], float(1)],
                     [[cap2], [cap1, cap2, cap3], float(1)],
                     [[cap3], [cap1, cap2, cap3, cap4], float(1)],
                     [[cap4], [cap1, cap2, cap3, cap4, cap5], float(1)],
                     [[cap1], [cap1, cap5], float(1 / 1)],
                     [[cap1, cap2], [cap1, cap4, cap5], float(1 / 2)],
                     [[cap1, cap2, cap3], [cap1, cap4, cap5], float(1 / 3)],
                     [[cap1, cap2, cap3, cap4], [cap1, cap5], float(1 / 4)],
                     [[cap1, cap2, cap3, cap4, cap5], [cap2], float(1 / 5)],
                     [[cap1, cap2, cap3, cap4, cap5], [cap3], float(1 / 5)],
                     [[cap1, cap2, cap3, cap4, cap5], [cap4], float(1 / 5)],
                     [[cap1, cap2, cap3, cap4, cap5], [cap5], float(1 / 5)]
                     ]
        for scenario in scenarios:
            reqd, given, factor = scenario
            iter_count = 1
            if reqd is not None:
                if len(reqd) > 1:
                    iter_count *= len(reqd)
            if given is not None:
                if len(given) > 1:
                    iter_count *= len(given)

            for _ in range(iter_count):
                if reqd is not None:
                    np.random.shuffle(reqd)
                if given is not None:
                    np.random.shuffle(given)
                logging.info("Required [{}]  Given [{}] expected {}".format(reqd, given, factor))
                self.assertEqual(factor,
                                 Capability.equivalence_factor(required_capabilities=reqd, given_capabilities=given))
        return

    @staticmethod
    def _factory() -> Capability:
        """
        Generate a random instance of a UniqueWorkRef
        :return: A new UniqueWorkRef
        """
        return SimpleCapability(uuid=UniqueRef().ref, capability_name=Gibberish.word_gibber())

    def test_pubsub_transport(self):
        """
        Generate 1000 random capabilities and ensure that all serialize/deserialize correctly.
        The requires the containerized test Kafka Service to be running locally.
        """
        expected = list()
        actual = list()
        expected, actual = TestKPubSub.kpubsub_test(msg_factory=self._factory,
                                                    num_msg=50,
                                                    msg_map_url=kpubsubai.MSG_MAP_URL)
        self.assertTrue(len(expected) == len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
        return


if __name__ == "__main__":
    unittest.main()
