from abc import abstractmethod
import threading
import logging
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotification import WorkNotification
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.state import State


class Agent(SrcSink):
    WORK_TIMER = float(0.05)

    _running = True

    @classmethod
    def running(cls, running: bool = None) -> bool:
        """
        Global start/stop for all Agents - if running is True then all Agents can schedule work event timers
        else no work timers are scheduled.
        :param running: Optional bool to set state of running
        :return: the value of running before applying the new run state if given.
        """
        pv = cls._running
        if running is not None:
            cls._running = running
        return pv

    def __init__(self):
        """
        Check this or child class has correctly implemented callable __call__ as needed to handle both the
        PubSub listener events and the work timer events.
        """
        super().__init__()

        self._work_timer = Agent.WORK_TIMER
        self._timer = None
        self._task_consumption_policy = None

        return

    def _work_notification(self) -> None:
        """
        If there is work to do then reset the work notification timer for the outstanding work.
        """
        if Agent.running():
            to_do = self._work_to_do()
            if to_do is not None:
                self._timer = threading.Timer(self._work_timer, self, args=[to_do]).start()
        return

    @abstractmethod
    @purevirtual
    def _do_notification(self,
                         task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can optionally grab the task from the
        task pool and work on it or ignore it.
        :param task_notification: The notification event for task requiring attention
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work(self,
                 work_notification: WorkNotification) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work_initiate(self,
                          work_notification: WorkNotification) -> None:
        """
        Handle the initiation the given work item from this agent
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work_finalise(self,
                          work_notification: WorkNotification) -> None:
        """
        Take receipt of the given completed work item that was initiated from this agent and do any
        final processing.
        """
        pass

    @abstractmethod
    @purevirtual
    def _work_to_do(self) -> WorkNotification:
        """
        Are there any tasks associated with the Agent that need working on ?
        :return: A WorkNotification event or None if there is no work to do
        """
        pass

    def __del__(self):
        """
        Clean up timer
        """
        if self._timer is not None:
            self._timer.cancel()
            self._timer = None
        pass

    @abstractmethod
    @purevirtual
    def work_initiate(self,
                      work_notification: WorkNotification) -> None:
        """
        Initiate the given work item with the agent as the owner of the work.
        """
        pass

    @property
    def task_consumption_policy(self) -> TaskConsumptionPolicy:
        """
        Get the policy that the agent uses to decide to process (or not) the task based on tasks meta data
        :return: The consumption policy
        """
        return self._task_consumption_policy

    @task_consumption_policy.setter
    def task_consumption_policy(self,
                                p: TaskConsumptionPolicy) -> None:
        """
        Set the policy that the agent uses to decide to process (or not) the task based on tasks meta data
        """
        self._task_consumption_policy = p

    @abstractmethod
    @purevirtual
    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        pass

    # ----- P R O P E R T I E S -----

    @property
    @abstractmethod
    @purevirtual
    def name(self) -> str:
        """
        The unique name of the Agent
        :return: The Agent name
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        pass

    @abstractmethod
    @purevirtual
    @property
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        pass

    @abstractmethod
    @purevirtual
    @property
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        pass

    @property
    def work_interval(self) -> float:
        """
        The wait period between doing work.
        :return: Wait interval between work timer events in seconds
        """
        return self._work_timer

    @work_interval.setter
    def work_interval(self,
                      t: float) -> None:
        """
        The rate at which completed tasks fail.
        :param t: the new work timer value in seconds (or fraction of second)
        """
        if t is None:
            self._work_timer = Agent.WORK_TIMER
        elif t <= float(0):
            msg = "Work timer must not be greater than or equal to zero, value given {}".format(t)
            logging.critical(msg)
            raise ValueError(msg)
        self._timer = float(t)
