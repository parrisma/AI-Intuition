from abc import ABC, abstractmethod
from journey10.task import Task
from journey10.state import State


class Actor(ABC):

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        The number of tasks remaining to work on
        :return: Number of remaining tasks
        """
        pass

    @abstractmethod
    def task_in(self,
                task: Task) -> None:
        """
        Adds the task to the Actor to-do list
        Raise a TaskException if the given task is not in the 'from_state'
        :param task: The task to be added to the to do list
        """
        pass

    @abstractmethod
    def do_work(self) -> None:
        """
        Work on the current task & pass it to the task out queue when finished.
        """
        pass

    @abstractmethod
    def task_out(self) -> Task:
        """
        Return a task that has finished it's given state or None if no tasks are finished.
        :return: A task that has been processed to end of it's current state or None if no such tasks are ready.
        """
        pass

    @property
    @abstractmethod
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        pass

    @property
    @abstractmethod
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        pass
