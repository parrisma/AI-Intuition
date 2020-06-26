from typing import Dict
from abc import ABC, abstractmethod
from journey11.src.lib.purevirtual import purevirtual


class EnvBuilder(ABC):
    ElasticDbConnectionContext = 'ElasticConnection'

    @abstractmethod
    @purevirtual
    def execute(self,
                context: Dict) -> None:
        """
        Execute actions to build the element of the environment owned by this builder
        :param context: Dictionary of current environment context that can be used or added to by builder
        :return: None: Implementation should throw and exception to indicate failure
        """
        pass

    @abstractmethod
    @purevirtual
    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages 
        :return: immutable UUID
        """
        pass

    @abstractmethod
    @purevirtual
    def __str__(self) -> str:
        """
        String representation of the Builder
        :return: Class rendered as a string
        """
        pass

    @abstractmethod
    @purevirtual
    def __repr__(self) -> str:
        """
        String representation of the Builder
        :return: Class rendered as a string
        """
        pass
