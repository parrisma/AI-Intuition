import random
from AIIntuition.journeys.journey5.compute import Compute
from AIIntuition.journeys.journey5.policy import Policy
from AIIntuition.journeys.journey5.task import Task


class SequentialPolicy(Policy):

    def __init__(self,
                 compute1: Compute,
                 compute2: Compute):
        self._idx = None
        self._comp_list = [compute1, compute2]

    def select_optimal_compute(self, task: Task) -> Compute:
        """
        return the computes in sequence
        :return: The Compute to associated the task with
        """
        if self._idx is None:
            self._idx = 0
        else:
            self._idx += 1

        if self._idx >= len(self._comp_list):
            raise IndexError('No more hosts remain to be selected')
        return self._comp_list[self._idx]
