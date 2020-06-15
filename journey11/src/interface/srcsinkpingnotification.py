from abc import abstractmethod
from typing import List
from journey11.src.interface.notification import Notification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy


class SrcSinkPingNotification(Notification):
    @property
    @abstractmethod
    @purevirtual
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference of the sender of the ping this is the response to
        :return: The work reference
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def src_sink(self) -> SimpleSrcSinkProxy:
        """
        The SrcSink that is the subject of the notification
        :return: The SimpleSrcSinkProxy
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def responder_address_book(self) -> List[SimpleSrcSinkProxy]:
        """
        The portion of the responders address book they wish to share with the ping sender.
        :return: List of zero or more SimpleSrcSinkProxy
        """
        pass
