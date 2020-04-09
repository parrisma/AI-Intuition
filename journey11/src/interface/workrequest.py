from abc import ABC, abstractmethod
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.notification import Notification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class WorkRequest(Notification):
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
    def originator(self) -> SrcSink:
        """
        The SrcSink participant that originating (sender) the request
        :return: The originating (sender) SrcSink of teh request
        """
        pass
