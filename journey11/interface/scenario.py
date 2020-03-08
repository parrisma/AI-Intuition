from abc import ABC, abstractmethod
from typing import List
from interface.task import Task


class Scenario(ABC):
    @abstractmethod
    def tasks(self) -> List[Task]:
        """
        Return the tasks defined for this scenario.
        :return: a scenario
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        pass
