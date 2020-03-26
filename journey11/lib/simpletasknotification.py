from journey11.interface.srcsink import SrcSink
from journey11.interface.tasknotification import TaskNotification
from journey11.interface.taskmetadata import TaskMetaData
from journey11.lib.uniqueworkref import UniqueWorkRef


class SimpleTaskNotification(TaskNotification):

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 task_meta: TaskMetaData,
                 notification_src_sink: SrcSink):
        self._work_ref = unique_work_ref
        self._task_meta = task_meta
        self._src_sink = notification_src_sink

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
    def src_sink(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._src_sink

    def __str__(self):
        """
        Render as string
        :return: String rendering of class instance
        """
        return "Task Notification for task id: {} from SrcSink {}".format(self._task_meta.task_id, self.src_sink.name)
