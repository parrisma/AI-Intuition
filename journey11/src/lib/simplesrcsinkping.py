from typing import Iterable, List
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.uniqueref import UniqueRef


class SimpleSrcSinkPing(SrcSinkPing):

    def __init__(self,
                 sender_srcsink: SrcSink,
                 required_capabilities: List[Capability]):
        self._work_ref = UniqueWorkRef(sender_srcsink.name, UniqueRef().ref)
        self._sender_srcsink = sender_srcsink
        self._required_capabilities = required_capabilities
        return

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def sender_srcsink(self) -> SrcSink:
        """
        The SrcSink that is the sender of the ping notification
        :return: The Player
        """
        return self._sender_srcsink

    @property
    def required_capabilities(self) -> Iterable[Capability]:
        """
        The required list of capabilities to respond to the ping. If capabilities is None or
        empty the matcher is allowed to consider this as match anything i.e. wild card.
        :return: The collection of required capabilities
        """
        return self._required_capabilities
