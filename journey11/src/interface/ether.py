from typing import Iterable
from abc import abstractmethod
import threading
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.srcsinknotification import SrcSinkNotification
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.notification import Notification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.notificationhandler import NotificationHandler


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
        super().__init__()
        self._call_lock = threading.Lock()
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._srcsink_notification, SrcSinkNotification)
        # self._handler.register_activity(handler_for_activity=self._do_pub,
        #                                activity_interval=Ether.PUB_TIMER,
        #                                activity_name="{}-do_pub_activity".format(ether_name))
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
    def _srcsink_notification(self,
                              ping_notification: SrcSinkNotification) -> None:
        """
        Handle a ping response from a player
        :param: The srcsink notification
        """
        pass

    @purevirtual
    @abstractmethod
    def _srcsink_ping(self,
                      ping_request: SrcSinkPing) -> None:
        """
        Handle a ping request from a player
        :param: The srcsink ping request
        """
        pass

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

    @property
    @purevirtual
    @abstractmethod
    def srcsinks(self) -> Iterable[SrcSink]:
        """
        The list of SrcSink known to the Ether
        :return: Players
        """
        pass
