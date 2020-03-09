from typing import Iterable, List
import threading
from journey11.interface.taskpool import TaskPool
from journey10.interface.task import Task


class SimpleTaskPool(TaskPool):

    def __init__(self,
                 tasks: Iterable[Task] = None):
        self._tasks = list()
        self._task_lock = threading.Lock()
        if tasks is not None:
            self.add(tasks)
        return

    def add(self,
            tasks: Iterable[Task]) -> None:
        """
        Add a task to the task pool
        :param tasks: The tasks to be added.
        """
        if tasks is not None:
            for t in tasks:
                if t is not None:
                    with self._task_lock:
                        self._tasks.append(t)
        return

    def match(self,
              pattern: str) -> List[Task]:
        """
        Return tasks from the task pool that match the given patter
        :param pattern: The pattern that tasks should match to be returned
        :return: List of matching tasks.
        """
        tl = list()
        with self._task_lock:
            if len(self._tasks) > 0:
                tl.append(self._tasks.pop())
        return tl
