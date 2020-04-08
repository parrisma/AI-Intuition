from abc import ABC, abstractmethod
from journey11.src.interface.notification import Notification
from journey11.src.interface.task import Task
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class WorkNotification(Notification):
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
    def task(self) -> Task:
        """
        The task to work on
        :return: The task
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def originator(self) -> SrcSink:
        """
        The SrcSink that orinated the notification
        :return: The SrcSink originator
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def source(self) -> SrcSink:
        """
        The SrcSink that orinated the notification
        :return: The SrcSink originator
        """
        pass
