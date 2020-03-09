from abc import ABC, abstractmethod
from typing import Iterable
from journey10.interface.task import Task
from journey11.interface.agent import Agent


class Scenario(ABC):
    @abstractmethod
    def tasks(self) -> Iterable[Task]:
        """
        Return the tasks defined for this scenario.
        :return: a iterable of tasks
        """
        pass

    @abstractmethod
    def agents(self) -> Iterable[Task]:
        """
        Return the agents that will do work.
        :return: a iterable of agents
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        pass
