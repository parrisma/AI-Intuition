from typing import Iterable
from abc import ABC, abstractmethod
from journey11.src.interface.scenario import Scenario


class ScenarioFactory(ABC):

    @abstractmethod
    def list_all(self) -> Iterable[Scenario]:
        """
        Return an iterable collection of all scenarios known to the factory
        :return:
        """
        pass
