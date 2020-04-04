from journey11.interface.task import Task
from journey11.interface.srcsink import SrcSink
from journey11.interface.worknotification import WorkNotification
from journey11.lib.uniqueworkref import UniqueWorkRef


class SimpleWorkNotification(WorkNotification):

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 task: Task,
                 task_pool: SrcSink):
        self._work_ref = unique_work_ref
        self._task = task
        self._task_pool = task_pool

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def task(self) -> Task:
        """
        The task the notification event relates to
        :return: The task
        """
        return self._task

    @property
    def src_sink(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._task_pool

    def __str__(self):
        """
        Render as string
        :return: String rendering of class instance
        """
        return "Work Notification for task id: {} from SrcSink".format(self._task.id, self._task_pool.name)
