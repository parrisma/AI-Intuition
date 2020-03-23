from journey11.interface.task import Task
from journey11.interface.workinitiate import WorkInitiate


class SimpleWorkInitiate(WorkInitiate):

    def __init__(self,
                 task: Task):
        self._task = task

    @property
    def task(self) -> Task:
        """
        The task to be initiated
        :return: The task being injected to be worked on.
        """
        return self._task
