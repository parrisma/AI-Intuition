from abc import ABC, abstractmethod
from journey11.interface.srcsink import SrcSink
from journey11.lib.purevirtual import purevirtual
from journey11.interface.taskmetadata import TaskMetaData
from journey11.lib.uniqueworkref import UniqueWorkRef


class TaskNotification(ABC):
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
    def src_sink(self) -> SrcSink:
        """
        The SrcSink participant that originated the Notification.
        :return: The originating SrcSink
        """
        pass
