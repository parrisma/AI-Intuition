import uuid
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
        return "{} : {}".format(self.__class__.__name__, self._as_str)

    def __str__(self):
        return self._as_str()

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self._equivalent(other))
