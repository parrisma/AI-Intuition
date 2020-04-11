from abc import ABC, abstractmethod
from datetime import datetime
from journey11.src.interface.srcsink import SrcSink
from journey11.src.lib.purevirtual import purevirtual


class SrcSinkMetaData(ABC):

    @property
    @abstractmethod
    @purevirtual
    def last_ping(self) -> datetime:
        """
        The datetime of the last ping from the SrcSink
        :return: Date Time of last SrcSink ping
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def srcsink(self) -> SrcSink:
        """
        The SrcSink the Meta data relates to.
        :return: SrcSink.
        """
        pass
