from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.taskmetadata import TaskMetaData
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SimpleTaskNotification(TaskNotification):

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 task_meta: TaskMetaData,
                 originator: SrcSink):
        self._work_ref = unique_work_ref
        self._task_meta = task_meta
        self._originator = originator

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def task_meta(self) -> TaskMetaData:
        """
        The task id the notification event relates to
        :return: The task id
        """
        return self._task_meta

    @property
    def originator(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._originator

    def __str__(self):
        """
        Render as string
        :return: String rendering of class instance
        """
        return "Task Notification for task id: {} from SrcSink {}".format(self._task_meta.task_id, self.originator.name)
