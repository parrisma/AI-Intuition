from abc import ABC, abstractmethod
from typing import Iterable
from journey10.interface.task import Task
from journey11.lib.purevirtual import purevirtual


class Scenario(ABC):
    @abstractmethod
    @purevirtual
    def tasks(self) -> Iterable[Task]:
        """
        Return the tasks defined for this scenario.
        :return: a iterable of tasks
        """
        pass

    @abstractmethod
    @purevirtual
    def agents(self) -> Iterable[Task]:
        """
        Return the agents that will do work.
        :return: a iterable of agents
        """
        pass

    @abstractmethod
    @purevirtual
    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        pass
