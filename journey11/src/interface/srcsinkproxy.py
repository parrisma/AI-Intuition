from abc import ABC, abstractmethod
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
