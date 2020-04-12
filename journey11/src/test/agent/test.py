import unittest
import time
import logging
from pubsub import pub
from journey11.src.interface.capability import Capability
from journey11.src.lib.state import State
from journey11.src.lib.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.lib.simplecapability import SimpleCapability
from journey11.src.test.agent.testagent import TestAgent
from journey11.src.test.task.testtask import TestTask
from journey11.src.test.agent.dummysrcsink import DummySrcSink


class TestTheAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        print("SetUp")
        TestTask.global_sync_reset()
        return

    def test_basic_capability(self):
        test_agent = TestAgent('agent {}'.format(1),
                               start_state=State.S0,
                               end_state=State.S1,
                               capacity=1,
                               task_consumption_policy=GreedyTaskConsumptionPolicy(),
                               trace=True)
        self.assertEqual(float(1),
                         Capability.equivalence_factor([SimpleCapability(CapabilityRegister.ETHER.name)],
                                                       test_agent.capabilities))
        return

    def test_simple_task_injection(self):
        effort = 3
        capacity = 1
        pool_name = "Dummy-Test-Pool"
        source_name = "Dummy-Test-Source"
        TestTask.process_start_state(State.S0)
        TestTask.process_end_state(State.S1)

        for i in range(3):
            logging.info("\n\n- - - - - T E S T  C A S E {} - - - -\n\n".format(i))
            test_task = TestTask(effort=effort)

            test_agent = TestAgent('agent {}'.format(i),
                                   start_state=State.S0,
                                   end_state=State.S1,
                                   capacity=capacity,
                                   task_consumption_policy=GreedyTaskConsumptionPolicy(),
                                   trace=True)

            test_notification = SimpleWorkNotificationDo(UniqueWorkRef(work_item_ref=pool_name,
                                                                       subject_name=str(test_task.id)),
                                                         originator=DummySrcSink(pool_name),
                                                         source=DummySrcSink(source_name),
                                                         task=test_task)
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

            tlid = TestAgent.trace_log_id("_do_work", type(test_notification), test_notification.work_ref)
            self.assertEqual(test_agent.trace_log[tlid], effort)

            tlid = TestAgent.trace_log_id("_do_notification", type(test_notification), test_notification.work_ref)
            self.assertTrue(tlid not in test_agent.trace_log)

            self.assertEqual(test_task.lead_time, int(effort / capacity))
        return


if __name__ == "__main__":
    unittest.main()
