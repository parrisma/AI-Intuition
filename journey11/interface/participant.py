from abc import ABC, abstractmethod
from journey11.interface.taskpool import TaskPool


class Participant(ABC):

    @abstractmethod
    def consume(self,
                task_pool: TaskPool) -> None:
        """
        Consume a task from the current task pool.
        """
        pass
