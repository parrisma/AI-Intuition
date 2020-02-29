from abc import ABC, abstractmethod
from typing import Tuple, Dict
from collections.abc import Iterable
from journey5.policy import Policy
from journey5.caseproperty import CaseProperty


class Case(ABC):
    _case = None

    def __init__(self):
        if self._case is None:
            self._case = self  # Record the reference to the current Test case.
        else:
            raise RuntimeError(self.__class__.__name__ + ' is a Singleton and can only have one instantiation')
        return

    @classmethod
    @abstractmethod
    def set_up(cls) -> Tuple[int, int, Policy, Iterable, int]:
        """
        Set-up the environment for a schedule test case.
            Note: The DataCenters, Hosts & Apps are available to the caller via the Class methods on these Types
            that return lists of all objects of the given type.
        :return:
            The number of hosts created
            The number of applications created
            The Host Selection Policy used by the scheduler
            The Host iterator used by the scheduler
            The number of 24 hour periods to run the schedule simulation for
        """
        raise NotImplementedError

    @abstractmethod
    def properties(self) -> Dict[CaseProperty, object]:
        """
        A dictionary of properties for the test case.
        :return: A dictionary of properties
        """
        raise NotImplementedError

    @classmethod
    def current_case(cls) -> 'Case':
        if cls._case is None:
            raise RuntimeError(cls.__class__.__name__ + ' is a Singleton that has not yet been instantiated')
        return cls._case
