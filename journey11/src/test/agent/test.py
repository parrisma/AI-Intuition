import unittest
import time
import logging
from math import ceil
from pubsub import pub
from journey11.src.interface.capability import Capability
from journey11.src.lib.state import State
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.main.simple.simpleagent import SimpleAgent
from journey11.src.main.simple.simpletask import SimpleTask
from journey11.src.test.agent.dummysrcsink import DummySrcSink
from journey11.src.main.simple.simpleether import SimpleEther
from journey11.src.main.simple.simpletaskpool import SimpleTaskPool
from journey11.src.main.simple.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.main.simple.simpleworknotificationinitiate import SimpleWorkNotificationInitiate
from journey11.src.main.simple.simpleworknotificationfinalise import SimpleWorkNotificationFinalise


class TestTheAgent(unittest.TestCase):
    _ether = None
    _task_pool = None
    _i = 1

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        print("SetUp")
        self._ether = SimpleEther("TestEther-{}".format(self._i))
        self._task_pool = SimpleTaskPool("TestTaskPool-{}".format(self._i))
        self._i += 1
        return

    def tearDown(self) -> None:
        pub.unsubAll()
        if self._ether is not None:
            del self._ether
        if self._task_pool is not None:
            del self._task_pool
        return

    def test_basic_capability(self):
        test_agent = SimpleAgent('agent {}'.format(1),
                                 start_state=State.S0,
                                 end_state=State.S1,
                                 capacity=1,
                                 task_consumption_policy=GreedyTaskConsumptionPolicy(),
                                 trace=True)
        time.sleep(1)  # Time for Agent discovery to settle.
        self.assertEqual(float(1),
                         Capability.equivalence_factor([SimpleCapability(CapabilityRegister.AGENT.name)],
                                                       test_agent.capabilities))
        return

    def test_ping_cycle(self):
        scenarios = [[[SimpleCapability(str(CapabilityRegister.AGENT))], 1],
                     [[], 1],
                     [[SimpleCapability(str(CapabilityRegister.POOL))], 0],
                     [[SimpleCapability("MadeUpCapability")], 0]]

        for scenario in scenarios:
            reqd_cap, expected_notification = scenario
            logging.info("\n\nTesting Ping Cycle with capabilities [{}]\n\n".format(str(reqd_cap)))
            sa = SimpleAgent('test agent',
                             start_state=State.S0,
                             end_state=State.S1,
                             capacity=1,
                             task_consumption_policy=GreedyTaskConsumptionPolicy(),
                             trace=True)
            time.sleep(.5)

            ping_srcsink = DummySrcSink("PingSrcSink", ping_topic=sa.topic)
            ping_workref = ping_srcsink.send_ping(required_capabilities=reqd_cap)

            time.sleep(1)
            self.assertEqual(expected_notification, len(ping_srcsink.ping_notifications))
            if expected_notification > 0:
                self.assertEqual(ping_workref.id, ping_srcsink.ping_notifications[0].work_ref.id)
            pub.unsubAll()
        return

    def test_simple_task_injection(self):
        effort = 3
        capacity = 1
        source_name = "Dummy-Test-Source-Inject"
        SimpleTask.process_start_state(State.S0)
        SimpleTask.process_end_state(State.S1)

        for i in range(3):
            logging.info("\n\n- - - - - T E S T  C A S E {} - - - -\n\n".format(i))
            test_task = SimpleTask(effort=effort)
            test_srcsink = DummySrcSink(source_name)

            test_agent = SimpleAgent('agent {}'.format(i),
                                     start_state=State.S0,
                                     end_state=State.S1,
                                     capacity=capacity,
                                     task_consumption_policy=GreedyTaskConsumptionPolicy(),
                                     trace=True)

            test_notification = SimpleWorkNotificationDo(UniqueWorkRef(suffix=source_name,
                                                                       prefix=str(test_task.id)),
                                                         originator=test_agent,
                                                         source=test_srcsink,
                                                         task=test_task)
            time.sleep(1)
            if i == 0:
                # Publish to agent via it's private topic.
                # test_agent(test_notification)
                pub.sendMessage(topicName=test_agent.topic, notification=test_notification)
            elif i == 1:
                # Direct Injection.
                test_agent._do_work(test_notification)
            else:
                # With Agent as callable
                test_agent(test_notification)

            time.sleep(1)

            tlid = SimpleAgent.trace_log_id("_do_work", type(test_notification), test_notification.work_ref)
            self.assertEqual(test_agent.trace_log[tlid], effort)

            tlid = SimpleAgent.trace_log_id("_do_notification", type(test_notification), test_notification.work_ref)
            self.assertTrue(tlid not in test_agent.trace_log)

            self.assertEqual(test_task.lead_time, int(ceil(effort / capacity)))

            work_done = test_agent.work_done
            self.assertEqual(1, len(work_done))
            self.assertEqual(test_task.id, work_done[0].task.id)
        return

    def test_simple_task_initiate(self):
        effort = 5
        capacity = 2
        SimpleTask.process_start_state(State.S0)
        SimpleTask.process_end_state(State.S1)

        logging.info("\n\n- - - - - T E S T  C A S E - I N I T I A T E - - - -\n\n")
        test_task = SimpleTask(effort=effort)

        test_agent = SimpleAgent('agent-initiate-1',
                                 start_state=State.S0,
                                 end_state=State.S1,
                                 capacity=capacity,
                                 task_consumption_policy=GreedyTaskConsumptionPolicy(),
                                 trace=True)
        time.sleep(.5)
        test_initiate = SimpleWorkNotificationInitiate(task=test_task, originator=test_agent)

        pub.sendMessage(topicName=test_agent.topic, notification=test_initiate)
        time.sleep(1)

        tlid = SimpleAgent.trace_log_id("_do_work_initiate", type(test_initiate), test_task.id)
        self.assertEqual(test_agent.trace_log[tlid], test_task.id)

        tlid = SimpleAgent.trace_log_id("_do_work_finalise", SimpleWorkNotificationFinalise, test_task.id)
        self.assertEqual(test_agent.trace_log[tlid], test_task.id)

        self.assertEqual(test_task.lead_time, int(ceil(effort / capacity)))

        work_done = test_agent.work_done
        self.assertEqual(1, len(work_done))
        self.assertEqual(test_task.id, work_done[0].task.id)
        return


if __name__ == "__main__":
    unittest.main()
