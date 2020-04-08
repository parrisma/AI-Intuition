from abc import abstractmethod
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.taskmetadata import TaskMetaData
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class TaskNotification(Notification):
    @property
    @abstractmethod
    @purevirtual
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def task_meta(self) -> TaskMetaData:
        """
        The task id the notification event relates to
        :return: The task id
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def originator(self) -> SrcSink:
        """
        The SrcSink participant that originated the Notification.
        :return: The originating SrcSink
        """
        pass
