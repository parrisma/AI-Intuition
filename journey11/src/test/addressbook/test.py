import unittest
import logging
import time
from pubsub import pub
from journey11.src.lib.addressbook import AddressBook
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.agent.dummysrcsink import DummySrcSink
from journey11.src.main.simple.simplecapability import SimpleCapability


class TestAddressBook(unittest.TestCase):
    _id = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestAddressBook._id))
        TestAddressBook._id += 1
        return

    def tearDown(self) -> None:
        pub.unsubAll()

    def test_basics(self):
        test_srcsink = DummySrcSink("DummySrcSink-1")
        test_address_book = AddressBook()

        self.assertEqual(0, len(test_address_book.get()))

        test_address_book.update(test_srcsink)
        self.assertEqual(1, len(test_address_book.get()))
        self.assertTrue(test_srcsink in test_address_book.get())
        return

    def test_get_with_capabilities_bad_params(self):
        test_address_book = AddressBook()

        with self.assertRaises(ValueError):
            test_address_book.get_with_capabilities(required_capabilities=[SimpleCapability("NotImportantForThisTest")],
                                                    match_threshold=-0.1)
        with self.assertRaises(ValueError):
            test_address_book.get_with_capabilities(required_capabilities=[SimpleCapability("NotImportantForThisTest")],
                                                    match_threshold=1.1)
        with self.assertRaises(ValueError):
            test_address_book.get_with_capabilities(required_capabilities=[SimpleCapability("NotImportantForThisTest")],
                                                    match_threshold=.5,
                                                    n=0)
        with self.assertRaises(ValueError):
            test_address_book.get_with_capabilities(required_capabilities=[SimpleCapability("NotImportantForThisTest")],
                                                    match_threshold=.5,
                                                    n=-1)
        return

    def test_get_with_capabilities_partial_matches(self):
        test_address_book = AddressBook()

        cap1 = SimpleCapability("Cap1")
        cap2 = SimpleCapability("Cap2")
        cap3 = SimpleCapability("Cap3")
        cap4 = SimpleCapability("Cap4")
        capx = SimpleCapability("Cap?")

        ss1 = DummySrcSink("DummySrcSink-1")
        ss1.capabilities = [cap1]

        ss2 = DummySrcSink("DummySrcSink-2")
        ss2.capabilities = [cap1, cap2]

        ss3 = DummySrcSink("DummySrcSink-3")
        ss3.capabilities = [cap1, cap2, cap3]

        ss4 = DummySrcSink("DummySrcSink-4")
        ss4.capabilities = [cap2, cap4]

        test_address_book.update(ss1)
        time.sleep(.01)
        test_address_book.update(ss2)
        time.sleep(.01)
        test_address_book.update(ss3)
        time.sleep(.01)
        test_address_book.update(ss4)

        scenarios = [[1, [cap1, capx], 1.0, [None], 1],
                     [2, [cap1, cap2, cap3], 1.0, [ss3], 1],
                     [3, [cap1, cap2], 1.0, [ss3], 1],  # As ss-3 also has Cap1, Cap2 and was created last
                     [4, [capx], 0.0, [ss4], 1],  # Zero => match any so will return last one created
                     [5, [capx], 0.3142, [None], 1],
                     [6, [capx], 1.0, [None], 1],
                     [7, [cap1], 1.0, [ss3], 1],
                     [8, [cap1, cap2], 1.0, [ss3], 1],
                     [9, [cap1, cap2], 0.5, [ss4], 1],
                     [10, [cap1], 1.0, [ss3, ss2], 2],
                     [11, [cap1], 1.0, [ss3, ss2, ss1], 3],
                     [12, [cap1], 1.0, [ss3, ss2, ss1], 4],
                     [13, [cap1], 0.0, [ss4, ss3, ss2, ss1], 4],
                     [14, [cap1], 1.0, [ss3, ss2, ss1], 5],
                     [15, [cap1], 1.0, [ss3, ss2, ss1], 500],
                     [16, [cap4, capx], 1.0, [None], 10],
                     [17, [cap4, capx], 0.5, [ss4], 10],
                     [18, [cap3, cap4, capx], 1.0, [None], 10],
                     [19, [cap3, cap4, capx], 0.33, [ss4, ss3], 10]
                     ]
        # TODO finish adding tests.

        for scenario in scenarios:
            case_num, caps, threshold, expected, n = scenario
            logging.info("test_get_with_capabilities_partial_matches case {}".format(case_num))
            res = test_address_book.get_with_capabilities(required_capabilities=caps,
                                                          match_threshold=threshold,
                                                          n=n
                                                          )
            if res is None:
                self.assertEqual(expected[0], res)
                self.assertEqual(len(expected), 1)
            else:
                self.assertEqual(len(expected), len(res))  # Should have same num results.
                for i in range(len(expected)):  # Order dependent equality.
                    self.assertEqual(expected[i], res[i])
            logging.info("case {} passed OK".format(case_num))

        return

    def test_get_with_capabilities_single_ss(self):
        test_srcsink = DummySrcSink("DummySrcSink-1")
        test_address_book = AddressBook()

        self.assertEqual(None, test_address_book.get_with_capabilities(test_srcsink.capabilities))
        test_address_book.update(test_srcsink)
        self.assertEqual(test_srcsink, test_address_book.get_with_capabilities(test_srcsink.capabilities)[0])
        return

    def test_get_with_capabilities_multi_ss(self):
        ss_list = list()
        for i in range(10):
            ss_list.append(DummySrcSink("DummySrcSink-{}".format(i)))

        # Confirm empty at create time.
        test_address_book = AddressBook()
        self.assertEqual(0, len(test_address_book.get()))

        # Confirm nothing matches empty address book in terms of capabilities
        for ss in ss_list:
            self.assertEqual(None, test_address_book.get_with_capabilities(ss.capabilities))

        # Add to the AddressBook with a time delay so the address timestamps are clearly different.
        # The last one added should always bethe one returned as it the last in time.
        for ss in ss_list:
            time.sleep(0.1)
            test_address_book.update(ss)
            self.assertEqual(ss, test_address_book.get_with_capabilities(ss.capabilities)[0])

        # Check everything is in the addressBook
        addr_bk = test_address_book.get()
        for ss in ss_list:
            self.assertTrue(ss in addr_bk)

        # Wait 5 seconds and then ask for items newer than 10 seconds - should be none
        delay = 2
        time.sleep(delay)
        ss_last = ss_list[-1]
        self.assertEqual(None,
                         test_address_book.get_with_capabilities(ss_last.capabilities, max_age_in_seconds=delay - 0.1))
        self.assertEqual(ss_last, test_address_book.get_with_capabilities(ss_last.capabilities, max_age_in_seconds=100)[0])

        # Add one more and make sure it comes back
        ss_new = DummySrcSink("DummySrcSink-new")
        test_address_book.update(ss_new)
        self.assertEqual(ss_new,
                         test_address_book.get_with_capabilities(ss_new.capabilities, max_age_in_seconds=None)[0])
        self.assertEqual(ss_new, test_address_book.get_with_capabilities(ss_new.capabilities, max_age_in_seconds=0.5)[0])
        return


if __name__ == "__main__":
    unittest.main()
