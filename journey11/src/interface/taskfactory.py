from abc import ABC, abstractmethod
from typing import List
from journey11.src.interface.task import Task
from journey11.src.lib.purevirtual import purevirtual


class TaskFactory(ABC):
    @abstractmethod
    @purevirtual
    def generate(self) -> List[Task]:
        """
        Generate one or more tasks
        :return: List of newly generated tasks.
        """
        pass
