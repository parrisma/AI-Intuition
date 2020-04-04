import unittest
import time
from journey11.src.lib.state import State
from journey11.src.lib.simpleworknotification import SimpleWorkNotification
from journey11.src.lib.greedytaskconsumptionpolicy import GreedyTaskConsumptionPolicy
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.loggingsetup import LoggingSetup
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

    def test_simple_task_injection(self):
        effort = 3
        capacity = 1
        pool_name = "Dummy-Test-Pool"
        test_task = TestTask(effort=effort)
        TestTask.process_start_state(State.S0)
        TestTask.process_end_state(State.S1)

        test_agent = TestAgent('agent 1',
                               start_state=State.S0,
                               end_state=State.S1,
                               capacity=capacity,
                               task_consumption_policy=GreedyTaskConsumptionPolicy())
        test_notification = SimpleWorkNotification(UniqueWorkRef(originator_id=pool_name,
                                                                 task_id=test_task.id),
                                                   originator=DummySrcSink(pool_name),
                                                   task=test_task)
        test_agent._do_work(test_notification)

        time.sleep(1)
        TestTask.global_sync_wait()

        self.assertEqual(test_task.lead_time, int(effort / capacity))


if __name__ == "__main__":
    unittest.main()
