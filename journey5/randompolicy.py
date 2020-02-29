import random
from journey5.compute import Compute
from journey5.policy import Policy
from journey5.task import Task


class RandomPolicy(Policy):

    def __init__(self):
        self._computes = None

    def select_optimal_compute(self, task: Task) -> Compute:
        """
        In this implemention a random compute is selected from all the available computes
        :return: The Compute to associated the task with
        """
        if self._computes is None:
            self._computes = Compute.all_compute_ids()
        rand_compute_id = random.randint(0, len(self._computes) - 1)
        return Compute.get_by_id(self._computes[rand_compute_id])
