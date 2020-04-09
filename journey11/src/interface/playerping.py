from abc import abstractmethod
from journey11.src.interface.notification import Notification
from journey11.src.interface.player import Player
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class PlayerPing(Notification):
    @property
    @abstractmethod
    @purevirtual
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def player(self) -> Player:
        """
        The Player that is the subject of the ping notification
        :return: The Player
        """
        pass