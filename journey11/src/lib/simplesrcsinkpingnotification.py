from typing import Iterable, List
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.uniqueref import UniqueRef


class SimpleSrcSinkNotification(SrcSinkPingNotification):

    def __init__(self,
                 responder_srcsink: SrcSink,
                 address_book: List[SrcSink],
                 sender_workref: UniqueWorkRef):
        self._work_ref = UniqueWorkRef(responder_srcsink.name, UniqueRef().ref)
        self._sender_srcsink = responder_srcsink
        self._address_book = address_book
        self._sender_workref = sender_workref
        return

    @property
    def responder_work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def sender_work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference of the sender of the ping this is the response to
        :return: The work reference
        """
        return self._sender_workref

    @property
    def src_sink(self) -> SrcSink:
        """
        The SrcSink that is replying to the ping.
        :return: The SrcSink
        """
        return self._sender_srcsink

    @property
    def responder_address_book(self) -> Iterable[SrcSink]:
        """
        The list of Players in the address book of the notification player
        :return: Zero or more players
        """
        return self._address_book
