from typing import List
from abc import abstractmethod
import threading
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.notification import Notification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.addressbook import AddressBook


class Ether(SrcSink):
    ETHER_BACK_PLANE_TOPIC = "ether-back-plane"
    PUB_TIMER = float(.25)

    def __init__(self,
                 ether_name: str):
        """
        Register the notification handlers and install publication activity.
            Note: Make sure properties name & topic are defined in the sub class before super().__inti__ is called
            otherwise the activity timer will reference non existent properties in the sub class as the timer
            will fire (here) before they have been defined in the sub-class init()
        """
        self._stopped = False
        self._address_book = AddressBook()
        super().__init__()
        self._call_lock = threading.Lock()
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._do_srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._do_srcsink_ping_notification, SrcSinkPingNotification)
        return

    def __del__(self):
        self._handler.activity_state(paused=True)
        return

    def __call__(self, notification: Notification):
        """ Handle notification requests
        :param notification: The notification to be passed to the handler
        """
        if isinstance(notification, Notification):
            self._handler.call_handler(notification)
        else:
            raise ValueError("{} un supported notification type for Task Pool".format(type(notification).__name__))
        return

    def stop(self) -> None:
        self._handler.activity_state(paused=True)
        return

    def start(self) -> None:
        self._handler.activity_state(paused=False)
        return

    @classmethod
    def back_plane_topic(cls) -> str:
        """
        The back-plane topic to which all Ether objects subscribe
        :return:
        """
        return cls.ETHER_BACK_PLANE_TOPIC

    @purevirtual
    @abstractmethod
    def _do_pub(self) -> None:
        """
        Publish any changes to known src sinks in the ether
        """
        pass

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

    def get_addressbook(self) -> List[SrcSink]:
        """
        The list of srcsinks known to the Ether
        :return: srcsinks
        """
        return self._address_book.get()

    def _update_addressbook(self,
                            srcsink: SrcSink) -> None:
        """
        Update the given src_sink in the collection of registered srcsinks. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        self._address_book.update(srcsink)
        return

    def _get_addresses_with_capabilities(self,
                                         required_capabilities: List[Capability]) -> List[SrcSink]:
        """
        Get the top five addresses in the address book that match the required capabilities. Always include
        this Ether (self) in the list.
        :param required_capabilities: The capabilities required
        :return: The list of matching addresses
        """
        addr = self._address_book.get_with_capabilities(required_capabilities=required_capabilities,
                                                        match_threshold=float(1),
                                                        max_age_in_seconds=600,
                                                        n=5)
        if addr is None:
            addr = list()
        addr.append(self)
        return addr
