from journey11.interface.task import Task
from journey11.interface.taskpool import TaskPool
from journey11.interface.worknotification import WorkNotification


class SimpleWorkNotification(WorkNotification):

    def __init__(self,
                 notification_task: Task,
                 notification_task_pool: TaskPool):
        self._task = notification_task
        self._task_pool = notification_task_pool

    @property
    def task(self) -> Task:
        """
        The task the notification event relates to
        :return: The task
        """
        return self._task

    @property
    def task_pool(self) -> TaskPool:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._task_pool
