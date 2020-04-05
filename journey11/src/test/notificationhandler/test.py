import unittest
import random
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.notificationhandler.testhandlegood import TestHandleGood
from journey11.src.test.notificationhandler.testtasknotification import TestTaskNotification
from journey11.src.test.notificationhandler.testworknotification import TestWorkNotification


class TestNotificationHandler(unittest.TestCase):
    _case = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        print("\n\n- - - - - - C A S E {} - - - - - - - - \n\n".format(TestNotificationHandler._case))
        TestNotificationHandler._case += 1

    def test_sig_checker_no_errors(self):
        try:
            thg = TestHandleGood()
            _ = NotificationHandler(object_to_be_handler_for=thg)
        except Exception as e:
            self.fail("Unexpected exception : [{}]".format(str(e)))

    def test_unregistered_type_err(self):
        thg = TestHandleGood(with_handler=True, throw_unhandled=True)
        self.assertRaises(NotImplementedError,
                          thg.__call__,
                          [float(0)])

    def test_routing(self):
        ths = list()
        for _ in range(5):
            ths.append(TestHandleGood(with_handler=True))  # Spin up with an embedded NotificationHandler

        for _ in range(100):
            for thg in ths:
                tn = TestTaskNotification()
                wn = TestWorkNotification()
                if random.random() > 0.5:
                    thg.__call__(tn)
                    thg.__call__(wn)
                else:
                    thg.__call__(wn)
                    thg.__call__(tn)
                self.assertEqual(tn.work_ref.id, thg.task_notif_sig)
                self.assertEqual(wn.work_ref.id, thg.work_notif_sig)


if __name__ == "__main__":
    unittest.main()
