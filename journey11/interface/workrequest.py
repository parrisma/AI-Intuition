from abc import ABC, abstractmethod
from journey11.interface.srcsink import SrcSink
from journey11.lib.purevirtual import purevirtual
from journey11.lib.uniqueworkref import UniqueWorkRef


class WorkRequest(ABC):
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
        The SrcSink participant that originating (sender) the request
        :return: The originating (sender) SrcSink of teh request
        """
        pass