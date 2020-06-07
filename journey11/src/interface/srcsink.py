from abc import ABC, abstractmethod
from typing import List
from journey11.src.interface.notification import Notification
from journey11.src.interface.capability import Capability
from journey11.src.lib.purevirtual import purevirtual


class SrcSink(ABC):

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
        The collection of capabilities of the SrcSink
        :return: The collection of capabilities
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_srcsink_ping_notification(self,
                                      ping_notification: Notification) -> None:
        """
        Handle a ping response from another SrcSink
        :param: The srcsink notification
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_srcsink_ping(self,
                         ping_request: Notification) -> None:
        """
        Handle a ping request from another SrcSink
        :param: The srcsink ping request
        """
        pass

    @purevirtual
    @abstractmethod
    def get_addressbook(self) -> List['SrcSink']:
        """
        The list of srcsinks known to the SrcSink
        :return: srcsinks
        """
        pass

    @purevirtual
    @abstractmethod
    def _update_addressbook(self,
                            srcsink: 'SrcSink') -> None:
        """
        Update the given src_sink in the collection of registered srcsinks. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        pass
