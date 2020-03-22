from abc import ABC, abstractmethod
from journey11.interface.task import Task
from journey11.interface.srcsink import SrcSink
from journey11.lib.purevirtual import purevirtual


class WorkNotification(ABC):
    @property
    @abstractmethod
    @purevirtual
    def task(self) -> Task:
        """
        The task to work on
        :return: The task
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def src_sink(self) -> SrcSink:
        """
        The SrcSink that orinated the notification
        :return: The SrcSink originator
        """
        pass
