from typing import List
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy


class SimpleSrcSinkPingNotification(SrcSinkPingNotification):
    # Annotation
    _work_ref: UniqueWorkRef
    _responder_srcsink_proxy: SimpleSrcSinkProxy
    _address_book: List[SimpleSrcSinkProxy]

    def __init__(self,
                 work_ref: UniqueWorkRef = None,
                 responder_srcsink: SrcSink = None,
                 address_book: List[SimpleSrcSinkProxy] = None):
        """
        Respond to a Ping request where responder capabilities match those requested
        :param work_ref: The work ref that initiated the intial ping
        :param responder_srcsink: The SrcSink of the responder
        :param address_book: Any SrcSinkProxies the responder wants to share
        Note: both params default None to allow proto serialisation
        """
        if work_ref is not None and responder_srcsink is not None and address_book is not None:
            self._work_ref = work_ref
            self._responder_srcsink_proxy = SimpleSrcSinkProxy(srcsink=responder_srcsink)
            self._address_book = address_book
        else:
            self._work_ref = None
            self._responder_srcsink_proxy = None
            self._address_book = None
        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def src_sink(self) -> SimpleSrcSinkProxy:
        """
        The SrcSink that is replying to the ping.
        :return: The SrcSink
        """
        return self._responder_srcsink_proxy

    @property
    def responder_address_book(self) -> List[SimpleSrcSinkProxy]:
        """
        The list of Players in the address book of the notification player
        :return: Zero or more players
        """
        return self._address_book

    def _as_str(self) -> str:
        return "SimpleSrcSinkPingNotification ref:{} for SrcSink: {}".format(str(self._work_ref),
                                                                             str(self._responder_srcsink_proxy))

    def __repr__(self) -> str:
        """
        String representation of SrcSinkPingNotification
        :return: SrcSinkPingNotification as string
        """
        return self._as_str()

    def __str__(self):
        """
        String representation of SrcSinkPingNotification
        :return: SrcSinkPingNotification as string
        """
        return self._as_str()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash("{}-{}".format(str(self._work_ref), str(self._responder_srcsink_proxy)))
        return self._hash

    def __eq__(self, other):
        if isinstance(other, self.__class__) and \
                self._work_ref == other._work_ref and \
                self._responder_srcsink_proxy == other._responder_srcsink_proxy:
            for s, o in zip(self._address_book, other._address_book):
                if s != o:
                    return False
        return True
