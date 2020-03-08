from abc import ABC, abstractmethod


class Capacity(ABC):
    @abstractmethod
    def capacity(self) -> int:
        """
        The work capacity of an actor
        :return: The work capacity as an integer
        """
        pass
