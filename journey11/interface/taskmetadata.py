from abc import ABC, abstractmethod
from journey11.lib.purevirtual import purevirtual


class TaskMetaData(ABC):

    @property
    @abstractmethod
    @purevirtual
    def task_id(self) -> int:
        """
        The task Id
        :return: Task Id
        """
        pass
