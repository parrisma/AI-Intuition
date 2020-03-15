from queue import Queue
from journey11.interface.agent import Agent
from journey11.lib.state import State
from journey11.interface.tasknotification import TaskNotification
from journey11.interface.worknotification import WorkNotification
from journey11.lib.simpleworknotification import SimpleWorkNotification


class TestAgent(Agent):
    FAIL_RATE = float(0)

    def __init__(self,
                 agent_name: str,
                 start_state: State,
                 end_state: State,
                 capacity: int):
        """
        """
        super().__init__()
        self._fail_rate = TestAgent.FAIL_RATE
        self._capacity = capacity
        self._work = Queue()
        self._agent_name = agent_name
        self._start_state = start_state
        self._end_state = end_state
        return

    def do_notification(self,
                        task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can optionally grab the task from the
        task pool and work on it or ignore it.
        :param task_notification: The notification event for task requiring attention
        """
        print("{} do_notification for task {} effort {}".format(self._agent_name, task_notification.task.id,
                                                                task_notification.task.effort))
        self._add_work_item_to_queue(SimpleWorkNotification(task_notification.task, task_notification.task_pool))
        return

    def do_work(self,
                work_notification: WorkNotification) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        print("{} do_work for task {}".format(self._agent_name, work_notification.task.id))
        self._work.task_done()
        if work_notification.task.do_work(self.capacity) > 0:
            self._add_work_item_to_queue(work_notification)
        return

    def _add_work_item_to_queue(self,
                                work_notification: WorkNotification) -> None:
        self._work.put(work_notification)
        super().work_notification()
        return

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        return

    def work_to_do(self) -> WorkNotification:
        """
        Are there any tasks associated with the Agent that need working on ?
        :return: A WorkNotification event or None if there is no work to do
        """
        wtd = SimpleWorkNotification(None, None)
        if not self._work.empty():
            wtd = self._work.get()
            print("{} work_to_do for task {}".format(self._agent_name, wtd.task.id))
        else:
            print("{} work_to_do - nothing to do".format(self._agent_name))
        return wtd

    def test_wait_until_done(self) -> None:
        self._work.join()
        return

        # ----- P R O P E R T I E S -----

    @property
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        return self._capacity

    @property
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        return self._start_state

    @property
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        return self._end_state

    @property
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        return self._fail_rate

    @failure_rate.setter
    def failure_rate(self,
                     r: float) -> None:
        """
        The rate at which completed tasks fail.
        :param r: the failure state of the actor
        """
        if r < 0.0 or r > 1.0:
            raise ValueError("Failure rate for Agent must be between 0.0 and 1.0")
        self._fail_rate = r
