from abc import ABC, abstractmethod
from journey11.lib.purevirtual import purevirtual
from journey11.interface.task import Task
from journey11.lib.state import State


class TaskPool(ABC):

    @purevirtual
    @abstractmethod
    def put_task(self,
                 task: Task) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state.
        :param task: The task to be added
        """
        pass

    @purevirtual
    @abstractmethod
    def get_task(self,
                 task: Task) -> None:
        """
        Pull a task out of the pool so it can be processed
        :param task: The task to get, None is returned if the task cannot be found (no longer in the pool)
        """
        pass

    @purevirtual
    @abstractmethod
    def topic_for_state(self,
                        state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def name(self) -> str:
        """
        The name of the task pool
        :return: The name of the task pool as string
        """
        pass
