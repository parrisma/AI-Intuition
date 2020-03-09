from abc import ABC, abstractmethod
from journey11.interface.agent import Agent


class SwarmEnv(ABC):
    @abstractmethod
    def associate(self,
                  participant: Agent) -> None:
        """
        Associate the given participant with teh Swarm.
        """
        pass
