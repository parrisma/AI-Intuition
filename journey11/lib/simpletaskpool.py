from typing import Iterable, List
import threading
from journey11.interface.taskpool import TaskPool
from journey11.interface.agent import Agent
from journey10.interface.task import Task


class SimpleTaskPool(TaskPool):
    # inner class.

    class TaskAllocation:
        def __init__(self,
                     task: Task,
                     agent: Agent):
            self._task = task
            self._agent = agent
            return

        @property
        def task(self) -> Task:
            return self._task

        @property
        def agent(self) -> Agent:
            return self._agent

    # Class Methods

    def __init__(self,
                 tasks: Iterable[Task] = None):
        self._tasks = list()
        self._update_lock = threading.Lock()
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
                    with self._update_lock:
                        self._tasks.append(t)
        return

    def subscribe(self,
                  pattern: str) -> List[Task]:
        """
        Return tasks from the task pool that match the given patter
        :param pattern: The pattern that tasks should match to be returned
        :return: List of matching tasks.
        """
        tl = list()
        with self._update_lock:
            if len(self._tasks) > 0:
                tl.append(self._tasks.pop())
        return tl

    def grab_task(self,
                  agent: Agent,
                  task_to_allocate: Task) -> bool:
        """
        Exclusively allocate the task to the given agent such that the agent can operate on the task. The agent
        must release the task when it is done processing it. If the task is already allocated to the agent then
        no action is taken.
        :param agent: The agent requesting the allocation.
        :param task_to_allocate:
        :return: True if the task was allocated; false means another agent is already allocated to the task
        """
        pass

    def release_task(self,
                     agent: Agent,
                     task_to_release: Task) -> None:
        """
        Release the task. If the task is not allocated no action is taken.
        :param agent: The agent releasing the task
        :param task_to_release: the task to release
        Exception is thrown if the agent requesting release is not the agent that was allocated the task
        """
        pass
