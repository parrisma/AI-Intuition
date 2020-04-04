import uuid
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotification import WorkNotification


class TestHandleGood(SrcSink):

    def __init__(self):
        super().__init__()
        self._name = "name:{}".format(str(uuid.uuid4()).replace('-', ''))
        self._topic = "topic:{}".format(str(uuid.uuid4()).replace('-', ''))

    def __call__(self, *args, **kwargs):
        return

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic

    def _do_notification(self,
                         task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can optionally grab the task from the
        task pool and work on it or ignore it.
        :param task_notification: The notification event for task requiring attention
        """
        pass

    def _do_work(self,
                 work_notification: WorkNotification) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        pass
