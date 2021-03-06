import uuid
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.lib.notificationhandler import NotificationHandler


class TestHandleGood(SrcSink):

    def __init__(self,
                 with_handler: bool = False,
                 throw_unhandled: bool = False):
        self._name = "name:{}".format(str(uuid.uuid4()).replace('-', ''))
        self._topic = "topic:{}".format(str(uuid.uuid4()).replace('-', ''))
        super().__init__()

        self._handler = None
        if with_handler:
            self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=throw_unhandled)
            self._handler.register_handler(self._do_notification, TaskNotification)
            self._handler.register_handler(self._do_work, WorkNotificationDo)

        self.task_notif_sig = None
        self.work_notif_sig = None

    def __call__(self, *args, **kwargs):
        # Pass the call handling to the Notification Handler.
        self._handler.call_handler(args[0])
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
        self.task_notif_sig = task_notification.work_ref.id

    def _do_work(self,
                 work_notification: WorkNotificationDo) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        self.work_notif_sig = work_notification.work_ref.id
