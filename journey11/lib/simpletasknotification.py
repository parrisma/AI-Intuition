from journey11.interface.srcsink import SrcSink
from journey11.interface.tasknotification import TaskNotification
from journey11.interface.taskmetadata import TaskMetaData


class SimpleTaskNotification(TaskNotification):

    def __init__(self,
                 notification_task_id: TaskMetaData,
                 notification_src_sink: SrcSink):
        self._task_meta = notification_task_id
        self._src_sink = notification_src_sink

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
