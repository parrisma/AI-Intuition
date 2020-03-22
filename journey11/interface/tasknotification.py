from abc import ABC, abstractmethod
from journey11.interface.srcsink import SrcSink
from journey11.lib.purevirtual import purevirtual
from journey11.interface.taskmetadata import TaskMetaData


class TaskNotification(ABC):
    @property
    @abstractmethod
    @purevirtual
    def task_meta(self) -> TaskMetaData:
        """
        The task the notification event relates to
        :return: The task
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
