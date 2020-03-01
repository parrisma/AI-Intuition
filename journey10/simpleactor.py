from copy import deepcopy, copy
import queue
import random
from journey10.state import State
from journey10.task import Task
from journey10.taskexception import TaskException
from journey10.actor import Actor
from journey10.capacity import Capacity


class SimpleActor(Actor):

    def __init__(self,
                 name: str,
                 from_state: State,
                 to_state: State,
                 failure_rate: float,
                 capacity: Capacity):
        """
        Actor Constructor.
        :param from_state:
        :param to_state:
        """
        self._name = name
        self._to_state = to_state
        self._from_state = from_state
        self._capacity = capacity
        self._work_capacity_orig = self._capacity.capacity()
        self._work_capacity = self._work_capacity_orig
        self._failure_rate_orig = failure_rate
        self._failure_rate = self._failure_rate_orig
        # This with mutable state
        self._queue_in = None
        self._queue_out = None
        self._current_task = None
        self.reset()
        return

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        self._queue_in = queue.Queue()
        self._queue_out = queue.Queue()
        self._current_task = None
        self._work_capacity = self._work_capacity_orig
        self._failure_rate = self._failure_rate_orig

    @property
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        curr_capacity = copy(self._work_capacity)
        self._work_capacity = self._capacity.capacity()
        return curr_capacity

    @property
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        return deepcopy(self._failure_rate)

    @failure_rate.setter
    def failure_rate(self,
                     f: bool) -> None:
        """
        The rate at which completed tasks fail.
        :param f: the failure state of the actor
        """
        self._failure_rate = deepcopy(f)

    @property
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        return deepcopy(self._from_state)

    @property
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        return deepcopy(self._to_state)

    @property
    def done(self) -> bool:
        """
        The number of tasks remaining to work on
        :return: Number of remaining tasks
        """
        return ((self._queue_in.qsize() + self._queue_out.qsize()) == 0) and (self._current_task is None)

    def task_in(self,
                task: Task) -> None:
        """
        Adds the task to the Actor to-do list
        Raise a TaskException if the given task is not in the 'from_state'
        :param task: The task to be added to the to do list
        """
        if task.state.value == self._from_state.value:
            self._queue_in.put_nowait(task)
        else:
            err = "Task should be in state [{0}] when given to this Actor".format(str(self._from_state))
            raise TaskException(err)
        return

    def do_work(self) -> None:
        """
        Work on the current task & pass it to the task out queue when finished.
        """
        if self._current_task is None:
            if not self._queue_in.empty():
                self._current_task = self._queue_in.get_nowait()

        if self._current_task is not None:
            remaining_effort = self._current_task.do_work(self.capacity)
            if remaining_effort == 0:
                self._current_task.state = self._to_state
                self._queue_out.put_nowait(self._current_task)
                self._current_task = None
        return

    def task_out(self) -> Task:
        t = None
        if not self._queue_out.empty():
            t = self._queue_out.get_nowait()
            if random.random() < self._failure_rate:
                t.failed = True
        return t

    def __str__(self) -> str:
        """
        Render the actor as a string
        :return: Actor as string
        """
        return "Actor[{0}] in [{1}] out[{2}] busy[{3}]".format(self._name,
                                                               str(self._queue_in.qsize()),
                                                               str(self._queue_out.qsize()),
                                                               str(self._current_task is not None))
