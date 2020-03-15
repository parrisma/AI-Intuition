from copy import deepcopy
import threading
from journey11.interface.task import Task
from journey11.lib.state import State


class TestTask(Task):
    _process_start_state = State.S0
    _process_terminal_state = State.S9
    _global_id = 1

    def __init__(self,
                 effort: int):
        """
        Constructor
        :param effort: The amount of effort needed to complete the task
        """
        self._state = TestTask._process_start_state
        self._id = TestTask._global_id
        TestTask._global_id += 1
        self._state_orig = self._process_start_state
        # Things with mutable state
        self._inital_effort = effort
        self._remaining_effort = None
        self._failed = None
        self._lead_time = None
        self._lock = threading.RLock()
        self.state = self._state_orig
        self.reset()

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        self._remaining_effort = self._inital_effort
        self._failed = False
        self._lead_time = float(0)
        self.state = self._state_orig
        if self._lock is not None:
            try:
                self._lock.release()
            except RuntimeError:
                pass  # Ignore error id lock i snot already aquired
        return

    @property
    def id(self) -> int:
        """
        The globally unique id of the task
        :return: Globally Unique id of the task
        """
        return self._id

    @property
    def lead_time(self) -> State:
        """
        The lead time between task starting and task finishing
        :return: Lead Time
        """
        with self._lock:
            lt = self._lead_time
        return lt

    @property
    def state(self) -> State:
        """
        Current State of the task.
        :return: Current State
        """
        return self._state

    @state.setter
    def state(self,
              s: State) -> None:
        """
        Set the tasks new state
        :param s: the state to set the task to
        """
        with self._lock:
            self._state = deepcopy(s)
            self._remaining_effort = 0
            if s.value != self._process_terminal_state.value:
                self._remaining_effort = self._inital_effort
        return

    @property
    def effort(self) -> int:
        """
        Current residual effort to complete current state
        :return: residual effort for current state
        """
        return self._remaining_effort

    @effort.setter
    def effort(self,
               e: int) -> None:
        """
        Set the residual effort.
        :param e: the residual effort
        """
        with self._lock:
            self._remaining_effort = e
        return

    @property
    def failed(self) -> bool:
        """
        True if task filed during processing
        :return: Failure state of task
        """
        return self._failed

    @failed.setter
    def failed(self,
               s: bool) -> None:
        """
        Set the failed status of the task
        :param s: the state to set the task to
        """
        self._failed = s

    def do_work(self,
                work: int) -> int:
        """
        Do the given units of work, i.e. decrement the number of work units from the residual effort remaining
        for the task. If the number of work units is greater than the residual then the difference of work
        units is 'lost' as the task will absorb any additional.
        :param work: The number of units of work to do.
        :return: The remaining units of work, where 0 means the task ne
        """
        with self._lock:
            self._remaining_effort = max(0, self._remaining_effort - work)
            self._lead_time += 1
            print("Task {} - Lead Time {}".format(self._id, self.lead_time))
        return self._remaining_effort

    def __str__(self) -> str:
        """
        Render the task as a string
        :return: Task as string
        """
        return "Task id[{0}] in State[{1}] @ effort[{2}] - Lead Time[{3}]".format(str(self._id),
                                                                                  str(self._state),
                                                                                  str(self._remaining_effort),
                                                                                  str(self._lead_time))

    @classmethod
    def process_start_state(cls,
                            start_state: State = None) -> State:
        if start_state is not None:
            cls._process_start_state = start_state
        return cls._process_start_state

    @classmethod
    def process_end_state(cls,
                          end_state: State = None) -> State:
        if end_state is not None:
            cls._process_terminal_state = end_state
        return cls._process_terminal_state
