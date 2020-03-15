from abc import ABC, abstractmethod
from journey11.interface.task import Task
from journey11.interface.taskpool import TaskPool
from journey11.lib.purevirtual import purevirtual


class TaskNotification(ABC):
    @property
    @abstractmethod
    @purevirtual
    def task(self) -> Task:
        """
        The task the notification event relates to
        :return: The task
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def task_pool(self) -> TaskPool:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        pass
