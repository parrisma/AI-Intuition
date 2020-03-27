from journey11.interface.srcsink import SrcSink
from journey11.interface.workrequest import WorkRequest
from journey11.lib.uniqueworkref import UniqueWorkRef


class SimpleWorkRequest(WorkRequest):

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 notification_src_sink: SrcSink):
        self._work_ref = unique_work_ref
        self._src_sink = notification_src_sink
        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

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
        return "Work Request {} from SrcSink {}".format(self._work_ref.id, self._src_sink.name)
