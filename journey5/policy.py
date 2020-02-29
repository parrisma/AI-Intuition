from abc import ABC, abstractclassmethod, abstractmethod
from journey5.compute import Compute
from journey5.task import Task


class Policy(ABC):
    @abstractmethod
    def select_optimal_compute(self,
                               task: Task) -> Compute:
        """
        Select the optimal compute for the given task
        :return: The Compute to associated the task with
        """
        raise NotImplementedError
