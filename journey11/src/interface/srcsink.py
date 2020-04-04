from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.reflection import Reflection


class SrcSink(ABC):

    def __init__(self):
        Reflection.check_method_exists(self, "__call__")
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
        :return: The unique SrcSink listen topic name
        """
        pass
