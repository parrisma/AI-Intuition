from journey11.test.agent.testagent import TestAgent
from journey11.test.task.testtask import TestTask
from journey11.lib.state import State
from journey11.lib.simpletasknotification import SimpleTaskNotification


def test_simple_task_injection():
    test_task = TestTask(effort=3)
    test_agent = TestAgent('agent 1', start_state=State.S0, end_state=State.S1)
    test_notification = SimpleTaskNotification(test_task, None)
    test_agent.do_notification(test_notification)


if __name__ == "__main__":
    test_simple_task_injection()
