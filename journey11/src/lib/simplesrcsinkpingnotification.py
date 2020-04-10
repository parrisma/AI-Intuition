from typing import Iterable, List
from journey11.src.interface.srcsinknotification import SrcSinkNotification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.uniqueref import UniqueRef


class SimpleSrcSinkNotification(SrcSinkNotification):

    def __init__(self,
                 sender_srcsink: SrcSink,
                 address_book: List[SrcSink]):
        self._work_ref = UniqueWorkRef(sender_srcsink.name, UniqueRef().ref)
        self._sender_srcsink = sender_srcsink
        self._address_book = address_book
        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def src_sink(self) -> SrcSink:
        """
        The SrcSink that is the subject of the notification
        :return: The SrcSink
        """
        return self._sender_srcsink

    @property
    def address_book(self) -> Iterable[SrcSink]:
        """
        The list of Players in the address book of the notification player
        :return: Zero or more players
        """
        return self._address_book
