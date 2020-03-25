from copy import deepcopy
import threading
from journey11.interface.task import Task
from journey11.lib.state import State


class TestTask(Task):
    _process_start_state = State.S0
    _process_terminal_state = State.S9
    _global_id = 1

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
        self._state = TestTask._process_start_state
        self._id = TestTask._global_id
        TestTask._global_id += 1
        if start_state is None:
            self._state_orig = self._process_start_state
        else:
            self._state_orig = start_state
        # Things with mutable state
        self._inital_effort = effort
        self._remaining_effort = None
        self._failed = None
        self._lead_time = None
        self._lock = threading.RLock()
        self._state = None
        self._trans = None
        self.reset()
        TestTask.global_sync_inc()

    @classmethod
    def global_sync_reset(cls) -> None:
        """
        Reset the Class sync status - this allows testing where the test needs to wait for all tasks
        to reach their terminal state before concluding
        :return:
        """
        cls._global_sync = 0
        cls._global_lock = threading.Lock()
        with cls._global_lock:
            cls._global_trigger = threading.Event()
        return

    @classmethod
    def global_sync_wait(cls) -> None:
        """
        Block until master trigger is released
        :return:
        """
        print("Waiting for global task completion Event")
        cls._global_trigger.wait()
        print("Global task completion Event done")
        return

    @classmethod
    def global_sync_inc(cls) -> None:
        """
        Task being constructed increments count
        :return:
        """
        with cls._global_lock:
            cls._global_sync += 1
        return

    @classmethod
    def global_sync_dec(cls) -> None:
        """
        Class moving into terminal process state decrements count. If all tasks have reached terminal state
        then release mater lock.
        :return:
        """
        with cls._global_lock:
            cls._global_sync -= 1
            if cls._global_sync == 0:
                cls._global_trigger.set()
        return

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        self._remaining_effort = self._inital_effort
        self._failed = False
        self._lead_time = float(0)
        self._state = self._state_orig
        self._trans = list()
        if self._lock is not None:
            try:
                self._lock.release()
            except RuntimeError:
                pass  # Ignore error id lock is not already acquired
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
                self._remaining_effort = self._inital_effort
            else:
                # Terminal process state
                TestTask.global_sync_dec()
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
                print("Task {} - Lead Time {}".format(self._id, self.lead_time))
            else:
                print("Task {} done in state {}".format(self._id, self.state))
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
