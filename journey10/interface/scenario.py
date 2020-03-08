from abc import ABC, abstractmethod
from typing import List
from interface.actor import Actor


class Scenario(ABC):
    @abstractmethod
    def get(self) -> List[List[Actor]]:
        """
        A reference to a scenario that can be passed to a simulator
        :return: a scenario
        """
        pass

    @abstractmethod
    def reset(self) -> None:
        """
        Reset the Scenario to it's initial state
        """
        pass
