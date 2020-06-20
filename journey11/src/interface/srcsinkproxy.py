from typing import List
from abc import ABC, abstractmethod
from journey11.src.interface.capability import Capability
from journey11.src.lib.purevirtual import purevirtual


class SrcSinkProxy(ABC):

    def __init__(self):
        return

    @property
    @purevirtual
    @abstractmethod
    def name(self) -> str:
        """
        The unique name of the SrcSink
        :return: The SrcSink name
        """
        pass

    @property
    @purevirtual
    @abstractmethod
    def topic(self) -> str:
        """
        The unique topic name that SrcSink listens on for activity specific to it.
        :return: The topic
        """
        pass

    @property
    @purevirtual
    @abstractmethod
    def capabilities(self) -> List[Capability]:
        """
        The capabilities of the SrcSink
        :return: A List of the SrcSink's capabilities
        """
        pass
