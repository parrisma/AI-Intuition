from abc import ABC, abstractmethod
from journey10.lib.state import State
from journey11.interface.taskpool import TaskPool


class Agent(ABC):

    @abstractmethod
    def do_work(self) -> None:
        """
        Work on the current task & pass it to the task out queue when finished.
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        pass

    # ----- P R O P E R T I E S -----

    @property
    @abstractmethod
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
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

    @property
    @abstractmethod
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        pass

    @failure_rate.setter
    @abstractmethod
    def failure_rate(self,
                     f: bool) -> None:
        """
        The rate at which completed tasks fail.
        :param f: the failure state of the actor
        """
        pass
