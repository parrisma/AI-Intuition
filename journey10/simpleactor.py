from copy import deepcopy
import queue
from journey10.state import State
from journey10.task import Task
from journey10.taskexception import TaskException
from journey10.actor import Actor


class SimpleActor(Actor):

    def __init__(self,
                 name: str,
                 from_state: State,
                 to_state: State):
        """
        Actor Constructor.
        :param from_state:
        :param to_state:
        """
        self._name = name
        self._to_state = to_state
        self._from_state = from_state
        self._queue_in = queue.Queue()
        self._queue_out = queue.Queue()
        self._current_task = None
        self._work_capacity = 1
        return

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
            remaining_effort = self._current_task.do_work(self._work_capacity)
            if remaining_effort == 0:
                self._current_task.state = self._to_state
                self._queue_out.put_nowait(self._current_task)
                self._current_task = None
        return

    def task_out(self) -> Task:
        t = None
        if not self._queue_out.empty():
            t = self._queue_out.get_nowait()
        return t

    def __str__(self) -> str:
        """
        Render the actor as a string
        :return: Actor as string
        """
        return "Actor[{0}] in [{1}] out[{2}]".format(self._name,
                                                     str(self._queue_in.qsize()),
                                                     str(self._queue_out.qsize()))
