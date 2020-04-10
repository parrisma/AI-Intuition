from abc import abstractmethod
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SrcSinkPing(Notification):
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
    def sender_srcsink(self) -> SrcSink:
        """
        The SrcSink that is the subject of the ping notification
        :return: The SrcSink
        """
