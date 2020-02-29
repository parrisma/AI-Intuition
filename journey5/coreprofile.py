from abc import ABC, abstractmethod
from AI-Intuition.journeys.journey5.cputype import CPUType


class CoreProfile(ABC):

    @property
    @abstractmethod
    def core_type(self) -> CPUType:
        """
        The CPU Type
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_count(self) -> int:
        """
        The number of cores.
        """
        raise NotImplementedError
