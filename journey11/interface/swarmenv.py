from abc import ABC, abstractmethod
from journey11.interface.agent import Agent
from journey11.lib.purevirtual import purevirtual


class SwarmEnv(ABC):
    @abstractmethod
    @purevirtual
    def associate(self,
                  participant: Agent) -> None:
        """
        Associate the given participant with teh Swarm.
        """
        pass
