import logging
import threading
import uuid
from copy import deepcopy
from journey11.src.interface.task import Task
from journey11.src.lib.state import State


class SimpleTask(Task):
    # Annotation
    _state: State
    _id: int
    _initial_effort: int
    _remaining_effort: int
    _failed: bool
    _lead_time: float
    _finalised: bool

    # Class level members
    _process_start_state = State.S0
    _process_terminal_state = State.S9

    _global_sync = 0
    _global_lock = None
    _global_trigger = None

    def __init__(self,
                 effort: int,
                 start_state: State = None):
        """
        Constructor
        :param effort: The amount of effort needed to complete the task
        """
        self._state = SimpleTask._process_start_state
        self._id = uuid.uuid1().int
        if start_state is None:
            self._state_orig = self._process_start_state
        else:
            self._state_orig = start_state
        # Things with mutable state
        self._initial_effort = effort
        self._remaining_effort = self._initial_effort
        self._failed = False
        self._lead_time = float(0)
        self._lock = threading.RLock()
        self._state = start_state
        self._trans = list()
        self._finalised = False

    @property
    def id(self) -> int:
        """
        The globally unique id of the task
        :return: Globally Unique id of the task
        """
        return self._id

    @property
    def lead_time(self) -> float:
        """
        The lead time between task starting and task finishing
        :return: Lead Time
        """
        return self._lead_time

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
            self._trans.append(self._state)
            self._state = deepcopy(s)
            self._remaining_effort = 0
            if s.value != self._process_terminal_state.value:
                self._remaining_effort = self._initial_effort
        return

    @property
    def work_in_state_remaining(self) -> int:
        """
        The units of work required to complete the current state
        :return: The units of work remaining in the current state
        """
        return self._remaining_effort

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

    @property
    def finalised(self) -> bool:
        """
        The finalised state of the task
        :return: True if task is flagged as finalised
        """
        return self._finalised

    @finalised.setter
    def finalised(self,
                  f: bool) -> None:
        """
        The finalised state of the task
        :param f: the task finalisation state to set
        """
        self._finalised = f

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
            if self.work_in_state_remaining > 0:
                self._remaining_effort = max(0, self.work_in_state_remaining - work)
                self._lead_time += 1
                logging.info("Task {} - Lead Time {}".format(self._id, self.lead_time))
            else:
                logging.info("Task {} done in state {}".format(self._id, self.state))
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
