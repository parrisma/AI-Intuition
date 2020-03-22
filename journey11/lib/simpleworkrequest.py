from journey11.interface.srcsink import SrcSink
from journey11.interface.workrequest import WorkRequest
from journey11.interface.taskmetadata import TaskMetaData


class SimpleWorkRequest(WorkRequest):

    def __init__(self,
                 notification_task_id: TaskMetaData,
                 notification_src_sink: SrcSink):
        self._task = notification_task_id
        self._src_sink = notification_src_sink

    @property
    def task_meta_data(self) -> TaskMetaData:
        """
        The task id the notification event relates to
        :return: The task id
        """
        return self._task

    @property
    def src_sink(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._src_sink
