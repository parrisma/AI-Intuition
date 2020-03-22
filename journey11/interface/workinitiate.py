from abc import ABC, abstractmethod
from journey11.lib.purevirtual import purevirtual
from journey11.interface.task import Task


class WorkInitiate(ABC):
    @property
    @abstractmethod
    @purevirtual
    def task(self) -> Task:
        """
        The task to be initiated
        :return: The task being injected yo be worked on.
        """
        pass
