import unittest
import logging
import time
from pubsub import pub
from journey11.src.lib.addressbook import AddressBook
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.agent.dummysrcsink import DummySrcSink


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

    def test_get_with_capabilities_single_ss(self):
        test_srcsink = DummySrcSink("DummySrcSink-1")
        test_address_book = AddressBook()

        self.assertEqual(None, test_address_book.get_with_capabilities(test_srcsink.capabilities))
        test_address_book.update(test_srcsink)
        self.assertEqual(test_srcsink, test_address_book.get_with_capabilities(test_srcsink.capabilities))
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
            self.assertEqual(ss, test_address_book.get_with_capabilities(ss.capabilities))

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
        self.assertEqual(ss_last, test_address_book.get_with_capabilities(ss_last.capabilities, max_age_in_seconds=100))

        # Add one more and make sure it comes back
        ss_new = DummySrcSink("DummySrcSink-new")
        test_address_book.update(ss_new)
        self.assertEqual(ss_new,
                         test_address_book.get_with_capabilities(ss_new.capabilities, max_age_in_seconds=None))
        self.assertEqual(ss_new, test_address_book.get_with_capabilities(ss_new.capabilities, max_age_in_seconds=0.5))
        return


if __name__ == "__main__":
    unittest.main()
