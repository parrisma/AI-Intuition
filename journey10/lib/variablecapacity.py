from typing import List
import numpy as np
from interface.capacity import Capacity


class VariableCapacity(Capacity):
    def __init__(self,
                 capacity: List[int],
                 pdf: List[float]):
        self._capacity = np.array(capacity)
        self._pdf = np.array(pdf)  # probability density function

        if len(self._capacity) != len(self._pdf):
            raise ValueError("The Probability Density Function and Capacity list must be of same length")
        if 1 - np.sum(self._pdf) > 1e-9:
            raise ValueError("Probability Density Function must sum to 1.0")
        return

    def capacity(self) -> int:
        """
        The work capacity of an actor
        :return: The work capacity as an integer, fixed at the rate given during construction.
        """
        var_cap = np.random.choice(a=self._capacity,
                                   size=1,
                                   p=self._pdf)
        return var_cap


if __name__ == "__main__":
    l = [4, 5, 6, 7, 8, 9]
    pdf = [.1, .1, .5, .1, .1, .1]
    vc = VariableCapacity(l, pdf)
    for i in range(0, 50):
        print(str(vc.capacity()))
