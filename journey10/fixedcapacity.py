from copy import copy
from journey10.capacity import Capacity


class FixedCapacity(Capacity):
    def __init__(self,
                 capacity: int):
        self._capacity = capacity
        return

    def capacity(self) -> int:
        """
        The work capacity of an actor
        :return: The work capacity as an integer, fixed at the rate given during construction.
        """
        return copy(self._capacity)
