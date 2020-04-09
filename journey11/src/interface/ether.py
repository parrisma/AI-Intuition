from typing import Iterable
from abc import abstractmethod
import threading
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.player import Player
from journey11.src.interface.playernotification import PlayerNotification
from journey11.src.interface.playerping import PlayerPing
from journey11.src.interface.notification import Notification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.notificationhandler import NotificationHandler


class Ether(SrcSink):
    PUB_TIMER = float(.25)

    def __init__(self,
                 ether_name: str):
        """
        Register the notification handlers and install publication activity.
        """
        super().__init__()
        self._call_lock = threading.Lock()
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._player_notification, PlayerNotification)
        self._handler.register_handler(self._player_ping, PlayerPing)
        self._handler.register_activity(handler_for_activity=self._do_pub,
                                        activity_interval=Ether.PUB_TIMER,
                                        activity_name="{}-do_pub_activity".format(ether_name))
        return

    def __del__(self):
        """
        Clean up
        """
        self._handler.stop_all_activity()
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

    @purevirtual
    @abstractmethod
    def _player_notification(self,
                             player_notification: PlayerNotification) -> None:
        """
        Handle a notification from a player that they are active in the ether
        :param: The player notification
        """
        pass

    @purevirtual
    @abstractmethod
    def _player_ping(self,
                     ping_notification: PlayerPing) -> None:
        """
        Handle a ping response from a player
        :param: The player notification
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_pub(self) -> None:
        """
        Publish any changes to known players in the ether
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
    def players(self) -> Iterable[Player]:
        """
        The list of players known to the Ether
        :return: Players
        """
        pass
