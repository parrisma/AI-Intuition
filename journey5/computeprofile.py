from abc import ABC, abstractmethod
from journey5.core import Core
from journey5.memory import Memory


class ComputeProfile(ABC):

    @property
    @abstractmethod
    def core(self) -> Core:
        """
        The Core Type Offered by the Compute resource
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def mem(self) -> Memory:
        """
        The memory offered by the compute
        """
        raise NotImplementedError
