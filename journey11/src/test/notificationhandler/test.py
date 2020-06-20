import unittest
import random
import logging
import time
from journey11.src.lib.notificationhandler import NotificationHandler
from src.lib.aitrace.trace import Trace
from journey11.src.test.notificationhandler.testhandlegood import TestHandleGood
from journey11.src.test.notificationhandler.testtasknotification import TestTaskNotification
from journey11.src.test.notificationhandler.testworknotification import TestWorkNotificationDo
from journey11.src.test.notificationhandler.dummycallable import DummyCallable


class TestNotificationHandler(unittest.TestCase):
    _case = 1

    @classmethod
    def setUpClass(cls):
        Trace()

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

    def test_back_off_exceptions(self):
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=0, max_interval=100, factor=2)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=-0.1, max_interval=100, factor=2)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=100, max_interval=0, factor=2)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=100, max_interval=-0.1, factor=2)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=10, max_interval=5, factor=2)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=1, max_interval=2, factor=0)
        with self.assertRaises(ValueError):
            NotificationHandler.back_off(reset=False, curr_interval=0, min_interval=1, max_interval=2, factor=-0.1)
        return

    def test_back_off_basics(self):
        minv = 3.1415
        new_i = NotificationHandler.back_off(reset=True, curr_interval=0, min_interval=minv, max_interval=100,
                                             factor=2)
        self.assertEqual(new_i, minv)
        return

    def test_back_off_limits(self):
        minv = 3.1415
        maxv = minv * 100.0
        new_i = 0
        for i in range(20):  # This a a power function show even with random factor should hit limit in < 10 iters.
            new_i = NotificationHandler.back_off(reset=False,
                                                 curr_interval=new_i,
                                                 min_interval=minv,
                                                 max_interval=maxv,
                                                 factor=2)
            logging.info("{} - new interval {}".format(i, new_i))
            self.assertTrue(new_i >= minv)
            self.assertTrue(new_i <= maxv)
        return

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
        for act in acts:
            # We expect each activity to have registered at least wait_cycle - 1 number of invocations.
            self.assertTrue(act.invocation_count >= (wait_cycles - 1))
        time.sleep(1)
        return

    def test_back_off_in_activity_handler(self):
        logging.info("\n\n- - - - - WITHOUT BACK OFF - - - - - \n\n")
        interval_in_sec = 0.25
        iterations = 5
        nh1 = NotificationHandler(object_to_be_handler_for=TestHandleGood())
        act1 = DummyCallable(with_back_off=False, intial_interval=interval_in_sec)
        nh1.register_activity(handler_for_activity=act1,
                              activity_interval=interval_in_sec)
        time.sleep(interval_in_sec * iterations)
        nh1.activity_state(paused=True)
        logging.info("Activity Count {}".format(act1.invocation_count))
        self.assertTrue(iterations - 1 <= act1.invocation_count <= iterations)
        del nh1
        del act1

        logging.info("\n\n- - - - - BACK OFF ENABLED - - - - - \n\n")
        interval_in_sec = 0.25
        max_interval = 2
        iterations = 20
        nh2 = NotificationHandler(object_to_be_handler_for=TestHandleGood())
        act2 = DummyCallable(with_back_off=True, intial_interval=interval_in_sec, max_interval=max_interval)
        nh2.register_activity(handler_for_activity=act2,
                              activity_interval=interval_in_sec)
        time.sleep(interval_in_sec * iterations)
        nh2.activity_state(paused=True)
        logging.info("Activity Count {}".format(act2.invocation_count))
        self.assertTrue(5 <= act2.invocation_count <= 10)
        del nh2
        del act2
        return


if __name__ == "__main__":
    unittest.main()
