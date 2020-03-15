from abc import ABC, abstractmethod
from typing import Iterable, List
from journey10.interface.task import Task
from journey11.interface.agent import Agent


class TaskPool(ABC):
    @abstractmethod
    def add(self,
            task: Iterable[Task]) -> None:
        """
        Add a task to the task pool
        :param task: The task to be added.
        """
        raise NotImplemented()

    @abstractmethod
    def subscribe(self,
                  pattern: str) -> List[Task]:
        """
        Return tasks from the task pool that match the given patter
        :param pattern: The pattern that tasks should match to be returned
        :return: List of matching tasks.
        """
        raise NotImplemented()

    @abstractmethod
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

    @abstractmethod
    def release_task(self,
                     agent: Agent,
                     task_to_release: Task) -> None:
        """
        Release the task. If the task is not allocated no action is taken.
        :param agent: The agent releasing the task
        :param task_to_release: the task to release
        Exception is thrown if the agent releasing is not the agent that task was allocated to
        """
        pass
