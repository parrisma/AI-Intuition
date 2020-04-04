from abc import ABC, abstractmethod
from journey11.lib.purevirtual import purevirtual
from journey11.interface.taskmetadata import TaskMetaData


class TaskConsumptionPolicy(ABC):
    @purevirtual
    @abstractmethod
    def process_task(self,
                     task_meta: TaskMetaData) -> bool:
        """
        Based on the given task meta data , return True if the policy recommends processing the task
        :return: True if polcy guidance is to process task
        """
        pass
