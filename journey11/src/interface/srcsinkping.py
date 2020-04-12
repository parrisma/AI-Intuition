from abc import abstractmethod
from typing import List
from journey11.src.interface.capability import Capability
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
        pass

    @property
    @abstractmethod
    @purevirtual
    def required_capabilities(self) -> List[Capability]:
        """
        The required list of capabilities to respond to the ping. If capabilities is None or
        empty the matcher is allowed to consider this as match anything i.e. wild card.
        :return: The collection of required capabilities
        """
        pass
