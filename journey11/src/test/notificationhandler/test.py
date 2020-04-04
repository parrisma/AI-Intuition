import unittest
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.test.notificationhandler.testhandlegood import TestHandleGood


class TestNotificationHandler(unittest.TestCase):

    def test_sig_checker_no_errors(self):
        thg = TestHandleGood()
        nh = NotificationHandler(thg)
        pass


if __name__ == "__main__":
    unittest.main()
