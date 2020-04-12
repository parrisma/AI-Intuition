from abc import abstractmethod
from typing import List
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SrcSinkPingNotification(Notification):
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
    def src_sink(self) -> SrcSink:
        """
        The SrcSink that is the subject of the notification
        :return: The SrcSink
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def address_book(self) -> List[SrcSink]:
        """
        The list of Players in the address book of the notification player
        :return: Zero or more players
        """
        pass
