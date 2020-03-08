from abc import ABC, abstractmethod
from typing import Iterable, List
from journey10.task import Task


class TaskPool(ABC):
    @abstractmethod
    def add(self,
            task: Iterable[Task]) -> None:
        """
        Add a task to the task pool
        :param task: The task to be added.
        """
        raise NotImplemented()

    @abstractmethod
    def match(self,
              pattern: str) -> List[Task]:
        """
        Return tasks from the task pool that match the given patter
        :param pattern: The pattern that tasks should match to be returned
        :return: List of matching tasks.
        """
        raise NotImplemented()
