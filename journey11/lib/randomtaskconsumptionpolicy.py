import logging
import random
from journey11.interface.taskmetadata import TaskMetaData
from journey11.interface.taskconsumptionpolicy import TaskConsumptionPolicy


class RandomTaskConsumptionPolicy(TaskConsumptionPolicy):
    def __init__(self,
                 skip_rate: float):
        if skip_rate < 0.0 or skip_rate > 1.0:
            msg = "Skip rate must be between 0.0 and 1.0 : {} was passed".format(skip_rate)
            logging.critical(msg)
            raise ValueError(msg)

        self._skip_rate = skip_rate
        return

    def process_task(self,
                     task_meta: TaskMetaData) -> bool:
        """
        Greedy policy always chooses to process task
        :return: True, always process task.
        """
        return random.random() <= self._skip_rate

    def __str__(self) -> str:
        return "Random Consmptn @ {}".format(self._skip_rate)
