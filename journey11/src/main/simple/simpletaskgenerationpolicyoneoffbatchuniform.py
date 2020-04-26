from typing import List
from journey11.src.interface.taskgenerationpolicy import TaskGenerationPolicy


class SimpleTaskGenerationPolicyOneOffBatchUniform(TaskGenerationPolicy):
    """
    Policy that dictates generation of a one off batch of given size.
    """

    def __init__(self,
                 batch_size: int,
                 effort: int):
        self._batch_size = batch_size
        self._effort = effort
        self._num_generated = 0
        return

    def num_to_generate(self) -> List[int]:
        """
        The number of tasks to generate
        :return: The number of tasks to generate
        """
        num_to_generate = self._batch_size - self._num_generated
        self._num_generated += num_to_generate
        return [self._effort] * num_to_generate
