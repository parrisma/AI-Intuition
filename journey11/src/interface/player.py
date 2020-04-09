from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual


class Player(ABC):

    @property
    @purevirtual
    @abstractmethod
    def name(self) -> str:
        """
        The unique name of the Player
        :return: The Player name
        """
        pass

    @property
    @purevirtual
    @abstractmethod
    def topic(self) -> str:
        """
        The unique topic name that Player listens on for activity specific to it.
        :return: The topic
        """
        pass
