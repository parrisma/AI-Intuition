import datetime
import threading
from abc import ABC, abstractmethod
from typing import List
from journey11.src.interface.notification import Notification
from journey11.src.interface.capability import Capability
from journey11.src.lib.purevirtual import purevirtual


class SrcSink(ABC):
    class SrcSinkWithTimeStamp:
        def __init__(self,
                     time_stamp: datetime,
                     srcsink: 'SrcSink'):
            self._time_stamp = time_stamp
            self._sender_src_sink = srcsink
            return

        @property
        def srcsink(self) -> 'SrcSink':
            return self._sender_src_sink

        @property
        def time_stamp(self) -> datetime:
            return self._time_stamp

        @time_stamp.setter
        def time_stamp(self,
                       t: datetime) -> None:
            self._time_stamp = t
            return

    def __init__(self):
        self._lock = threading.Lock()
        self._src_sinks_with_timestamp = dict()
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
    def _srcsink_ping_notification(self,
                                   ping_notification: Notification) -> None:
        """
        Handle a ping response from another SrcSink
        :param: The srcsink notification
        """
        pass

    @purevirtual
    @abstractmethod
    def _srcsink_ping(self,
                      ping_request: Notification) -> None:
        """
        Handle a ping request from another SrcSink
        :param: The srcsink ping request
        """
        pass

    @property
    def get_srcsink_addressbook(self) -> List['SrcSink']:
        """
        The list of srcsinks known to the Ether
        :return: srcsinks
        """
        with self._lock:
            srcsinks = list(x.srcsink for x in self._src_sinks_with_timestamp.values())
        return srcsinks

    def _update_srcsink_addressbook(self,
                                    sender_srcsink: 'SrcSink') -> None:
        """
        Update the given src_sink in the collection of registered srcsinks. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        srcsink_name = sender_srcsink.name
        with self._lock:
            if srcsink_name not in self._src_sinks_with_timestamp:
                self._src_sinks_with_timestamp[srcsink_name] = \
                    SrcSink.SrcSinkWithTimeStamp(srcsink=sender_srcsink,
                                                 time_stamp=datetime.datetime.now())
            else:
                self._src_sinks_with_timestamp[srcsink_name].time_stamp = datetime.datetime.now()
        return
