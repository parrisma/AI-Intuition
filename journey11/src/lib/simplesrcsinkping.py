from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.uniqueref import UniqueRef


class SimpleSrcSinkPing(SrcSinkPing):

    def __init__(self,
                 sender_srcsink: SrcSink):
        self._work_ref = UniqueWorkRef(sender_srcsink.name, UniqueRef().ref)
        self._sender_srcsink = sender_srcsink
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
