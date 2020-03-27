from abc import ABC, abstractmethod
import inspect
import threading
from journey11.lib.purevirtual import purevirtual
from journey11.lib.state import State
from journey11.interface.srcsink import SrcSink
from journey11.interface.tasknotification import TaskNotification
from journey11.interface.worknotification import WorkNotification


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
        cl = getattr(self, "__call__", None)
        if not callable(cl):
            raise NotImplemented("Must implement __call__(self, arg1)")
        else:
            # Check signature
            sig = inspect.signature(cl)
            if 'arg1' not in sig.parameters:
                raise NotImplemented("Must implement __call__(self, arg1)")

        self._work_timer = Agent.WORK_TIMER
        self._timer = None

        self._activity = list()

        return

    def __call__(self, arg1) -> None:
        """
        The agent is callable two contexts
        1. As the sink for PubSub in which case a TaskNotification will be passed
        2. As the handler for it's own timer to check if work needs to be done in which case WorkNotification is passed

        Other types for arg1 trigger a ValueError exception

        :param arg1: Either a TaskNotification or a WorkNotification
        """
        if isinstance(arg1, TaskNotification):
            msg = "{} Rx TaskNotification {}".format(self.name, arg1.work_ref.id)
            self._activity.append(msg)
            print(msg)
            self._do_notification(arg1)
        elif isinstance(arg1, WorkNotification):
            msg = "{} Rx WorkNotification {}".format(self.name, arg1.work_ref.id)
            self._activity.append(msg)
            print(msg)
            self._do_work(arg1)
        else:
            raise ValueError("Unexpected type [{}] passed to {}.__call__".format(type(arg1), self.__class__.__name__))
        return

    def work_notification(self) -> None:
        """
        If there is work to do then reset the work notification timer for the outstanding work.
        """
        if Agent.running():
            to_do = self.work_to_do()
            if to_do is not None:
                self._timer = threading.Timer(self._work_timer, self, args=[to_do]).start()
        return

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
    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        pass

    @abstractmethod
    @purevirtual
    def work_to_do(self) -> WorkNotification:
        """
        Are there any tasks associated with the Agent that need working on ?
        :return: A WorkNotification event or None if there is no work to do
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

    @property
    @abstractmethod
    @purevirtual
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        pass

    @failure_rate.setter
    @abstractmethod
    @purevirtual
    def failure_rate(self,
                     r: float) -> None:
        """
        The rate at which completed tasks fail.
        :param r: the failure state of the actor
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
            raise ValueError("Work timer must not be greater than or equal to zero")
        self._timer = float(t)
