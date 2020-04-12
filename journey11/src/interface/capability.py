import uuid
from typing import List
from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual


class Capability(ABC):

    def __init__(self):
        self._hash = hash(str(uuid.uuid4()).replace('-', ''))
        return

    @abstractmethod
    @purevirtual
    def value(self):
        """
        Return the 'value' of the capability
        :return: Capability value
        """
        pass

    @staticmethod
    def equivalence_factor(required_capabilities: List['Capability'],
                           given_capabilities: List['Capability']) -> float:
        """
        The degree in range 0.0 to 1.0 that the given capabilities match required capabilities
        :param required_capabilities:
        :param given_capabilities:
        :return: The degree to which required matches given
        """
        if required_capabilities is None or len(required_capabilities) == 0:
            return float(1)  # Nothing required so full match irrespective of given

        if given_capabilities is None or len(given_capabilities) == 0:
            return float(0)  # Nothing given so no match.

        equiv = 0
        for rc in required_capabilities:
            for gc in given_capabilities:
                if rc._equivalent(gc):
                    equiv += 1
        return equiv / len(required_capabilities)

    @abstractmethod
    @purevirtual
    def _as_str(self) -> str:
        """
        Render the capability as a string
        :return:
        """
        pass

    @abstractmethod
    @purevirtual
    def _equivalent(self,
                    other) -> bool:
        """
        Return true if the two capabilities are equivalent. Where 'equivalent' means separate entities both holding the
        capability would both be able to perform the same type of activity/work.
        :param other: Capability to compare to
        :return: True if capabilities are 'equivalent'
        """
        pass

    def __repr__(self):
        return "{}".format(self._as_str())

    def __str__(self):
        return self._as_str()

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self._equivalent(other))
