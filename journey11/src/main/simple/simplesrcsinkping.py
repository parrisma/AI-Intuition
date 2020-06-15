from typing import List
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkproxy import SrcSinkProxy
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.main.simple.simplesrcsinkproxy import SimpleSrcSinkProxy
from journey11.src.main.simple.simplecapability import SimpleCapability


class SimpleSrcSinkPing(SrcSinkPing):
    # Annotation
    _work_ref: UniqueWorkRef
    _sender_srcsink_proxy: SimpleSrcSinkProxy
    _required_capabilities: List[SimpleCapability]

    def __init__(self,
                 sender_srcsink: SrcSink = None,
                 required_capabilities: List[SimpleCapability] = None):
        """
        :param sender_srcsink: The Source Sink Acting as sender
        :param required_capabilities: The capabilities required by the receiver before responding
        Note: both params default None to allow proto serialisation
        """
        if sender_srcsink is not None and required_capabilities is not None:
            self._work_ref = UniqueWorkRef(prefix=sender_srcsink.name)
            self._sender_srcsink_proxy = SimpleSrcSinkProxy(srcsink=sender_srcsink)
            self._required_capabilities = required_capabilities
        else:
            self._work_ref = None
            self._sender_srcsink_proxy = None
            self._required_capabilities = None

        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def sender_srcsinkproxy(self) -> SrcSinkProxy:
        """
        The SrcSink that is the sender of the ping notification
        :return: The Player
        """
        return self._sender_srcsink_proxy

    @property
    def required_capabilities(self) -> List[Capability]:
        """
        The required list of capabilities to respond to the ping. If capabilities is None or
        empty the matcher is allowed to consider this as match anything i.e. wild card.
        :return: The collection of required capabilities
        """
        return self._required_capabilities

    def _as_str(self) -> str:
        return "SimpleSrcSinkPing ref:{} for SrcSink: {}".format(str(self._work_ref), str(self._sender_srcsink_proxy))

    def __repr__(self) -> str:
        """
        String representation of SrcSinkPing
        :return: SrcSinkPing as string
        """
        return self._as_str()

    def __str__(self):
        """
        String representation of SrcSinkPing
        :return: SrcSinkPing as string
        """
        return self._as_str()

    def __hash__(self):
        if self._hash is None:
            self._hash = hash("{}-{}".format(str(self._work_ref), str(self._sender_srcsink_proxy)))
        return self._hash

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               self._work_ref == other._work_ref and \
               self._sender_srcsink_proxy == other._sender_srcsink_proxy and \
               self._required_capabilities == other._required_capabilities
