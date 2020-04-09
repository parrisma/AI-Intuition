import unittest
import random
import logging
import time
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.notificationhandler.testhandlegood import TestHandleGood
from journey11.src.test.notificationhandler.testtasknotification import TestTaskNotification
from journey11.src.test.notificationhandler.testworknotification import TestWorkNotificationDo
from journey11.src.test.notificationhandler.dummycallable import DummyCallable


class TestNotificationHandler(unittest.TestCase):
    _case = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E {} - - - - - - - - \n\n".format(TestNotificationHandler._case))
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

    def test_multi_handler_err(self):
        try:
            thg = TestHandleGood()
            nh = NotificationHandler(object_to_be_handler_for=thg)
            nh.register_handler(handler_for_message=DummyCallable(), message_type=float)
        except Exception as e:
            self.fail("Unexpected exception : [{}]".format(str(e)))

        with self.assertRaises(ValueError):
            nh.register_handler(DummyCallable(), float)

        return

    def test_routing(self):
        ths = list()
        for _ in range(5):
            ths.append(TestHandleGood(with_handler=True))  # Spin up with an embedded NotificationHandler

        for _ in range(100):
            for thg in ths:
                tn = TestTaskNotification()
                wn = TestWorkNotificationDo()
                if random.random() > 0.5:
                    thg.__call__(tn)
                    thg.__call__(wn)
                else:
                    thg.__call__(wn)
                    thg.__call__(tn)
                self.assertEqual(tn.work_ref.id, thg.task_notif_sig)
                self.assertEqual(wn.work_ref.id, thg.work_notif_sig)

    def test_activity(self):
        interval_in_sec = 0.5
        wait_cycles = 4
        num_notif_handlers = 3
        num_activities_per_notif_handler = 10
        acts = list()
        nhs = list()
        for _ in range(num_notif_handlers):
            nhs.append(NotificationHandler(object_to_be_handler_for=TestHandleGood()))

        try:
            for nh in nhs:
                for _ in range(num_activities_per_notif_handler):
                    act = DummyCallable()
                    nh.register_activity(handler_for_activity=act,
                                         activity_interval=interval_in_sec)
                    acts.append(act)
        except Exception as e:
            self.fail("Unexpected exception : [{}]".format(str(e)))

        time.sleep(interval_in_sec * wait_cycles)  # Allow the timer to fire a few times
        for nh in nhs:
            nh.stop_all_activity()
        for act in acts:
            # We expect each activity to have registered at least wait_cycle - 1 number of invocations.
            self.assertTrue(act.invocation_count >= (wait_cycles - 1))
        time.sleep(1)
        return


if __name__ == "__main__":
    unittest.main()
