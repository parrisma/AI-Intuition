from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.notificationhandler import NotificationHandler


class SrcSink(ABC):

    def __init__(self):
        self._notification_handler = NotificationHandler(object_to_be_handler_for=self)
        return

    def __call__(self, *args, **kwargs):
        self._notification_handler.call_handler(args[0])
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
