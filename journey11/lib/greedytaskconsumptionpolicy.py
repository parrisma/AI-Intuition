from journey11.interface.taskmetadata import TaskMetaData
from journey11.interface.taskconsumptionpolicy import TaskConsumptionPolicy


class GreedyTaskConsumptionPolicy(TaskConsumptionPolicy):
    def process_task(self,
                     task_meta: TaskMetaData) -> bool:
        """
        Greedy policy always chooses to process task
        :return: True, always process task.
        """
        return True

    def __str__(self) -> str:
        return "Greedy Consmptn @ 100%"
