from abc import ABC, abstractmethod
from typing import List
from journey5.cputype import CPUType
from journey5.task import Task


class TaskProfile(ABC):

    @property
    @abstractmethod
    def max_mem(self) -> int:
        """
        The maximum Memory required by the Task
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def mem_volatility(self) -> float:
        """
        The volatility in range 0.0 to 1.0 of the memory demand with respect to the task load profile
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def cpu_type(self) -> CPUType:
        """
        The CPU type (ideally) required by the task
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def task_load(self) -> int:
        """
        The load factor placed on the compute
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def load_profile(self) -> Task.LoadProfile:
        """
        The Load profile (shape over time) of the Task
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def load_shape(self) -> List[float]:
        """
        24 (for each hour of day) Load factors in range 0.0 to 1.0
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def run_time(self) -> int:
        """
        The runtime in hours (elapsed) of the Task
        """
        raise NotImplementedError
