import unittest
import time
from pubsub import pub
from journey11.test.agent.testagent import TestAgent
from journey11.test.task.testtask import TestTask
from journey11.lib.state import State
from journey11.lib.simpletasknotification import SimpleTaskNotification


class TestTheAgent(unittest.TestCase):
    def test_simple_task_injection(self):
        return
        effort = 3
        capacity = 1
        test_task = TestTask(effort=effort)
        test_agent = TestAgent('agent 1', start_state=State.S0, end_state=State.S1, capacity=capacity)
        test_notification = SimpleTaskNotification(test_task, None)
        test_agent.do_notification(test_notification)

        test_agent.test_wait_until_done()  # Wait for all worker thread in Agent to complete

        self.assertEqual(test_task.lead_time, int(effort / capacity))

    def test_multi_task_multi_agent_via_pub(self):
        topic1 = "Topic1"
        topic2 = "Topic2"

        topic1_capacity = 2
        topic2_capacity = 1
        agents = [[TestAgent("agent 1", State.S0, State.S1, capacity=topic1_capacity), []],
                  [TestAgent("agent 2", State.S0, State.S1, capacity=topic2_capacity), []],
                  [TestAgent("agent 3", State.S0, State.S1, capacity=topic1_capacity), [topic1, topic2]],
                  [TestAgent("agent 4", State.S0, State.S1, capacity=topic1_capacity), []],
                  [TestAgent("agent 5", State.S0, State.S1, capacity=topic2_capacity), []]]

        for agent, topics in agents:
            for topic in topics:
                pub.subscribe(agent, topic)

        task1_effort = 8
        task2_effort = 4
        task1_list = list()
        task2_list = list()
        for i in range(1):
            test_task1 = TestTask(effort=task1_effort)
            test_task2 = TestTask(effort=task2_effort)
            pub.sendMessage(topicName=topic1, arg1=SimpleTaskNotification(test_task1, None))
            pub.sendMessage(topicName=topic2, arg1=SimpleTaskNotification(test_task2, None))
            task1_list.append(test_task1)
            task2_list.append(test_task2)

        print("Waiting for all agents to complete")
        for agent, _ in agents:
            agent.test_wait_until_done()
        time.sleep(2)
        print("Done, All agents to complete")

        task1_expected_lead_time = 2 * (task1_effort / topic1_capacity) + (
                (task1_effort + task2_effort) / topic1_capacity)

        task2_expected_lead_time = 2 * (task2_effort / topic2_capacity) + (
                (task1_effort + task2_effort) / topic1_capacity)

        for task in task1_list:
            print("Task {} lead time {}".format(task.id, task.lead_time))

        for task in task2_list:
            print("Task {} lead time {}".format(task.id, task.lead_time))

        return


if __name__ == "__main__":
    unittest.main()
