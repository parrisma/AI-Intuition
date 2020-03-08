from abc import ABC, abstractmethod
from journey11.interface.participant import Participant


class SwarmEnv(ABC):
    @abstractmethod
    def associate(self,
                  participant: Participant) -> None:
        """
        Associate the given participant with teh Swarm.
        """
        pass
